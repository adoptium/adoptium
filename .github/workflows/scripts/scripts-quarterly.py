#!/usr/bin/env python3
"""
Quarterly Contribution Impact Report Generator (Script-based fallback)

Fetches merged PRs across all Adoptium organization repositories within a date range,
analyzes contribution impact using sentiment analysis, and generates a markdown report.

Usage:
  python scripts/quarterly-report.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD [--org ORG]
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from github import Github, Auth
    from textblob import TextBlob
except ImportError:
    print("ERROR: Required packages not installed. Install with:")
    print("  pip install PyGithub textblob")
    exit(1)


def get_github_client(token: str = None) -> Github:
    """Initialize GitHub API client."""
    if token is None:
        token = os.environ.get("GH_TOKEN")
        if not token:
            raise ValueError(
                "GitHub token not provided. Set GH_TOKEN environment variable "
                "or pass --token argument."
            )
    auth = Auth.Token(token)
    return Github(auth=auth)


def parse_date(date_str: str) -> datetime:
    """Parse YYYY-MM-DD string to datetime object."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")


def is_bot(username: str) -> bool:
    """Check if a user is a bot based on username patterns."""
    bot_indicators = ["bot", "[bot]", "-bot", "action", "copilot"]
    return any(indicator in username.lower() for indicator in bot_indicators)


def calculate_sentiment(text: str) -> float:
    """Calculate sentiment polarity of text using TextBlob.
    
    Returns a score between -1.0 (negative) and 1.0 (positive).
    """
    try:
        if not text or not isinstance(text, str):
            return 0.0
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    except Exception:
        return 0.0


def fetch_quarterly_data(
    g: Github, org_name: str, start_date: datetime, end_date: datetime
) -> dict:
    """Fetch and aggregate PR and contribution data.
    
    Returns dict with:
      - total_prs: total merged PRs count
      - human_prs: dict of human contributor login -> PR count
      - bot_prs: dict of bot contributor login -> PR count
      - impact_scores: dict of contributor login -> sentiment impact score
      - top_prs: list of highest-impact PRs (title, author, repo)
    """
    org = g.get_organization(org_name)
    
    human_prs = {}
    bot_prs = {}
    impact_scores = {}
    all_prs = []
    total_prs = 0
    
    print(f"Fetching repositories in {org_name}...")
    repos = list(org.get_repos())
    print(f"Found {len(repos)} repositories.")
    
    for repo in repos:
        print(f"  Processing {repo.name}...")
        try:
            pulls = repo.get_pulls(state="closed")
            for pull in pulls:
                if pull.merged_at is None:
                    continue
                
                # Check if PR is within date range
                if not (start_date <= pull.merged_at <= end_date):
                    continue
                
                total_prs += 1
                author = pull.user.login
                is_bot_user = is_bot(author)
                
                # Track PR count
                if is_bot_user:
                    bot_prs[author] = bot_prs.get(author, 0) + 1
                else:
                    human_prs[author] = human_prs.get(author, 0) + 1
                
                # Calculate impact from PR comments
                pr_sentiment = 0.0
                comment_count = 0
                try:
                    comments = pull.get_issue_comments()
                    for comment in comments:
                        sentiment = calculate_sentiment(comment.body)
                        pr_sentiment += sentiment
                        comment_count += 1
                except Exception as e:
                    print(f"    Warning: Could not fetch comments for PR #{pull.number}: {e}")
                
                # Average sentiment or use PR title sentiment if no comments
                if comment_count > 0:
                    pr_sentiment = pr_sentiment / comment_count
                else:
                    pr_sentiment = calculate_sentiment(pull.title)
                
                if not is_bot_user:
                    impact_scores[author] = impact_scores.get(author, 0.0) + pr_sentiment
                
                # Store PR for top contributions list
                all_prs.append({
                    "number": pull.number,
                    "title": pull.title,
                    "author": author,
                    "repo": repo.name,
                    "sentiment": pr_sentiment,
                    "merged_at": pull.merged_at.isoformat(),
                })
        except Exception as e:
            print(f"    Error processing {repo.name}: {e}")
            continue
    
    # Sort PRs by sentiment for top contributions
    top_prs = sorted(all_prs, key=lambda x: x["sentiment"], reverse=True)[:10]
    
    return {
        "total_prs": total_prs,
        "human_prs": human_prs,
        "bot_prs": bot_prs,
        "impact_scores": impact_scores,
        "top_prs": top_prs,
        "all_prs": all_prs,
    }


def get_top_contributors(data: dict, top_n: int = 10) -> list:
    """Get top N contributors by PR count, optionally weighted by impact.
    
    Returns list of dicts with contributor info.
    """
    impact_scores = data["impact_scores"]
    human_prs = data["human_prs"]
    
    # Sort by PR count, then by impact score
    contributors = [
        {
            "login": login,
            "prs": count,
            "impact_score": impact_scores.get(login, 0.0),
        }
        for login, count in human_prs.items()
    ]
    
    contributors.sort(key=lambda x: (x["prs"], x["impact_score"]), reverse=True)
    return contributors[:top_n]


def generate_markdown_report(
    data: dict, start_date: datetime, end_date: datetime, org_name: str
) -> str:
    """Generate markdown report from collected data."""
    report = []
    report.append("# Quarterly Contribution Impact Report\n")
    report.append(f"**Period:** {start_date.date()} to {end_date.date()}")
    report.append(f"**Organization:** `{org_name}`\n")
    
    # Summary section
    report.append("## Summary\n")
    report.append(f"- **Total merged PRs:** {data['total_prs']}")
    report.append(f"- **Human contributors:** {len(data['human_prs'])}")
    report.append(f"- **Bot contributors:** {len(data['bot_prs'])}\n")
    
    # Top human contributors
    report.append("## Top 10 Contributors\n")
    top_contributors = get_top_contributors(data, top_n=10)
    if top_contributors:
        report.append("| Contributor | PRs | Impact Score |")
        report.append("|---|---|---|")
        for contributor in top_contributors:
            score_str = f"{contributor['impact_score']:.2f}" if contributor['impact_score'] else "0.00"
            report.append(
                f"| [@{contributor['login']}](https://github.com/{contributor['login']}) | "
                f"{contributor['prs']} | {score_str} |"
            )
        report.append("")
    else:
        report.append("No human contributions found in this period.\n")
    
    # Top contributions by impact
    report.append("## Top 10 Most Impactful Contributions\n")
    if data["top_prs"]:
        for i, pr in enumerate(data["top_prs"], 1):
            sentiment_emoji = "✅" if pr["sentiment"] > 0.1 else "⚠️" if pr["sentiment"] > 0 else "❌"
            report.append(
                f"{i}. [{pr['repo']}#{pr['number']}]("
                f"https://github.com/adoptium/{pr['repo']}/pull/{pr['number']}) "
                f"— {pr['title'][:60]}... by @{pr['author']} {sentiment_emoji}"
            )
        report.append("")
    else:
        report.append("No contributions found.\n")
    
    # Bot contributions
    if data["bot_prs"]:
        report.append("## Bot Contributions\n")
        report.append(f"- **Total bot PRs:** {sum(data['bot_prs'].values())}")
        report.append("\n| Bot | PRs |")
        report.append("|---|---|")
        for bot_name, count in sorted(data["bot_prs"].items(), key=lambda x: x[1], reverse=True):
            report.append(f"| {bot_name} | {count} |")
        report.append("")
    
    report.append("---\n")
    report.append("*This report was generated using the script-based fallback approach.*")
    
    return "\n".join(report)


def save_output_files(data: dict, report_markdown: str, output_dir: str = "/tmp/gh-aw/agent"):
    """Save report and data files for GitHub Actions workflow."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save markdown report
    report_path = Path(output_dir) / "report.md"
    report_path.write_text(report_markdown, encoding="utf-8")
    print(f"Saved report to {report_path}")
    
    # Save summary.json for workflow
    summary = {
        "total_merged_prs": data["total_prs"],
        "human_contributors": len(data["human_prs"]),
        "bot_contributors": len(data["bot_prs"]),
        "top_contributors": get_top_contributors(data, top_n=10),
        "bot_prs": data["bot_prs"],
        "report_generated_by": "script-fallback",
    }
    summary_path = Path(output_dir) / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Saved summary to {summary_path}")
    
    # Save all PRs for reference
    all_prs_path = Path(output_dir) / "all_prs.json"
    all_prs_path.write_text(json.dumps(data["all_prs"], indent=2), encoding="utf-8")
    print(f"Saved PR data to {all_prs_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate quarterly contribution impact report for Adoptium.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python scripts/quarterly-report.py --start-date 2026-01-01 --end-date 2026-03-31
  python scripts/quarterly-report.py --start-date 2026-01-01 --end-date 2026-03-31 --org myorg --token $GH_TOKEN
        """,
    )
    parser.add_argument(
        "--start-date",
        required=True,
        help="Start date for report window (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        required=True,
        help="End date for report window (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--org",
        default="adoptium",
        help="GitHub organization name (default: adoptium)",
    )
    parser.add_argument(
        "--token",
        help="GitHub API token (defaults to GH_TOKEN environment variable)",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp/gh-aw/agent",
        help="Output directory for generated files",
    )
    
    args = parser.parse_args()
    
    try:
        # Parse dates
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)
        
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")
        
        print(f"\n📊 Generating quarterly report for {args.org}")
        print(f"   Period: {start_date.date()} to {end_date.date()}\n")
        
        # Initialize GitHub client
        g = get_github_client(args.token)
        
        # Fetch data
        data = fetch_quarterly_data(g, args.org, start_date, end_date)
        
        # Generate report
        report = generate_markdown_report(data, start_date, end_date, args.org)
        
        # Save outputs
        save_output_files(data, report, args.output_dir)
        
        print(f"\n✅ Report generated successfully!\n")
        print(report)
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=__import__("sys").stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
