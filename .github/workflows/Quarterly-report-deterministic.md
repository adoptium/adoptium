---
description: Quarterly contribution impact report for the adoptium org. Data is fetched and aggregated deterministically; the agent only ranks and writes.
on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:
    inputs:
      start_date:
        description: "Report window start date (YYYY-MM-DD). Defaults to 90 days ago."
        required: false
        type: string
      end_date:
        description: "Report window end date (YYYY-MM-DD). Defaults to today (UTC)."
        required: false
        type: string
engine:
  id: copilot
timeout-minutes: 30
permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write
network:
  allowed:
    - defaults
steps:
  - name: Fetch and aggregate quarterly contribution data
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      INPUT_START_DATE: ${{ inputs.start_date }}
      INPUT_END_DATE: ${{ inputs.end_date }}
    # Keep this aggregation in sync with quarterly-report-fallback.yml
    run: |
      set -euo pipefail
      mkdir -p /tmp/gh-aw/agent

      SINCE="${INPUT_START_DATE:-}"
      UNTIL="${INPUT_END_DATE:-}"
      [ -n "$SINCE" ] || SINCE=$(date -u -d '90 days ago' '+%Y-%m-%d')
      [ -n "$UNTIL" ] || UNTIL=$(date -u '+%Y-%m-%d')
      for d in "$SINCE" "$UNTIL"; do
        echo "$d" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' \
          || { echo "::error::Invalid date '$d' (expected YYYY-MM-DD)"; exit 1; }
      done
      [ "$SINCE" \< "$UNTIL" ] || [ "$SINCE" = "$UNTIL" ] \
        || { echo "::error::start_date ($SINCE) is after end_date ($UNTIL)"; exit 1; }
      echo "Window: $SINCE..$UNTIL"

      MERGED_Q="org:adoptium is:pr is:merged merged:$SINCE..$UNTIL"
      ISSUES_Q="org:adoptium is:issue is:closed closed:$SINCE..$UNTIL"
      MERGED_TOTAL=$(gh api -X GET search/issues -f q="$MERGED_Q" -f per_page=1 --jq .total_count)
      ISSUES_TOTAL=$(gh api -X GET search/issues -f q="$ISSUES_Q" -f per_page=1 --jq .total_count)
      echo "Expected: $MERGED_TOTAL merged PRs, $ISSUES_TOTAL closed issues"

      # GitHub search occasionally returns an empty page with HTTP 200; retry rather
      # than silently producing a zero-count report. Pagination caps at 1000 results.
      fetch_search() { # $1=query $2=jq projection $3=outfile $4=expected total
        local attempt n
        for attempt in 1 2 3; do
          gh api -X GET search/issues -f q="$1" -f per_page=100 --paginate --jq "$2" \
            | jq -s '.' > "$3"
          n=$(jq length "$3")
          if [ "$n" -gt 0 ] || [ "$4" -eq 0 ]; then return 0; fi
          echo "attempt $attempt: got 0 of $4 results for '$1'; retrying in 10s"
          sleep 10
        done
        echo "::error::search returned no results for '$1' (expected $4)"
        return 1
      }

      fetch_search "$MERGED_Q" \
        '.items[] | {number, title, user: .user.login, repo: (.repository_url | sub("https://api.github.com/repos/"; "")), merged: .pull_request.merged_at}' \
        /tmp/gh-aw/agent/merged-prs.json "$MERGED_TOTAL"

      fetch_search "$ISSUES_Q" \
        '.items[] | {number, title, user: .user.login, repo: (.repository_url | sub("https://api.github.com/repos/"; ""))}' \
        /tmp/gh-aw/agent/closed-issues.json "$ISSUES_TOTAL"

      # Attribute Copilot-authored PRs to the guiding human (first non-Copilot assignee)
      jq -c '.[] | select(.user | test("^(Copilot|copilot-swe-agent(\\[bot\\])?)$"))' /tmp/gh-aw/agent/merged-prs.json \
        | while IFS= read -r pr; do
            repo=$(echo "$pr" | jq -r .repo)
            num=$(echo "$pr" | jq -r .number)
            guide=$(gh api "repos/$repo/issues/$num" \
              --jq '[.assignees[].login | select(test("copilot"; "i") | not)] | first // "unknown"' \
              2>/dev/null || echo "unknown")
            echo "$pr" | jq --arg g "$guide" '. + {on_behalf_of: $g}'
          done | jq -s '.' > /tmp/gh-aw/agent/copilot-prs.json

      jq -n \
        --arg since "$SINCE" \
        --arg until "$UNTIL" \
        --argjson merged_total "$MERGED_TOTAL" \
        --argjson issues_total "$ISSUES_TOTAL" \
        --slurpfile prs /tmp/gh-aw/agent/merged-prs.json \
        --slurpfile iss /tmp/gh-aw/agent/closed-issues.json \
        --slurpfile cp /tmp/gh-aw/agent/copilot-prs.json \
        '{
          window_start: $since,
          window_end: $until,
          total_merged_prs: $merged_total,
          total_closed_issues: $issues_total,
          fetched_merged_prs: ($prs[0] | length),
          truncated: (($prs[0] | length) < $merged_total or ($iss[0] | length) < $issues_total),
          repos_touched: ([$prs[0][].repo] | unique | length),
          prs_by_repo: ([$prs[0][].repo] | group_by(.) | map({repo: .[0], count: length}) | sort_by(-.count)),
          contributors: ([$prs[0][].user] | group_by(.) | map({user: .[0], merged_prs: length}) | sort_by(-.merged_prs)),
          copilot: {
            total_copilot_prs: ($cp[0] | length),
            by_guide: ([$cp[0][].on_behalf_of] | group_by(.) | map({guide: .[0], copilot_prs: length}) | sort_by(-.copilot_prs))
          }
        }' > /tmp/gh-aw/agent/summary.json

      echo "=== summary.json ==="
      cat /tmp/gh-aw/agent/summary.json
safe-outputs:
  create-issue:
    title-prefix: "[quarterly-impact] "
    labels: [report, quarterly-impact]
---

# Quarterly Contribution Impact Report

All GitHub data has already been fetched and aggregated for you before this step. Do NOT call any GitHub tools or shell commands to fetch data — everything you need is on disk.

## Pre-fetched data
- `/tmp/gh-aw/agent/summary.json` — pre-computed aggregates: the report window (`window_start`/`window_end`), totals, PRs grouped by repository, contributors ranked by merged-PR count, and Copilot PR counts grouped by the human who guided them. Read this first.
- `/tmp/gh-aw/agent/merged-prs.json` — the full list of merged PRs (number, title, author, repo) for detail in the highlights.
- `/tmp/gh-aw/agent/closed-issues.json` — closed issues over the window.
- `/tmp/gh-aw/agent/copilot-prs.json` — merged PRs authored by Copilot, each with `on_behalf_of`: the human who guided that work (`"unknown"` if no human assignee was found).

## Your task
Using only the files above, write a concise quarterly contribution impact report and create exactly one GitHub issue in this repository.

The contributors in `summary.json` are already ranked by merged-PR count. Treat that count as the base signal, but you may adjust the narrative ranking using PR titles in `merged-prs.json` where a contributor's work is clearly higher-impact. State your reasoning briefly.

## The issue must contain
- A header summary: the exact window covered (`window_start` to `window_end`), total merged PRs, total closed issues, and number of distinct repositories touched. If `truncated` is true in `summary.json`, note that the totals are exact but per-contributor and per-repo detail covers only the first `fetched_merged_prs` results (a GitHub search API limit).
- A "Copilot-assisted contributions" section from `summary.json`'s `copilot.by_guide`: how many Copilot-authored PRs were merged and who guided them, with a line for any attributed to "unknown". Omit the section only if there were no Copilot PRs.
- A ranked list of the top contributors by estimated impact, each with their merged-PR count and a one-line justification.
- A "Top 10 contributions" highlight section drawn from `merged-prs.json`, chosen for apparent impact based on titles.
- An "Activity by repository" section from `prs_by_repo`, listing the most active repositories.
- Suggested next steps or items needing maintainer attention for the next quarter.

## Constraints
- Create exactly one issue.
- Do not fetch any additional data; rank and summarize only what is on disk.
- Impact scoring is heuristic; flag anything that may warrant human review.
- Keep it concise and skimmable.
