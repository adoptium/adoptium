---
description: Quarterly contribution impact report for the adoptium org. Data is fetched and aggregated deterministically; the agent only ranks and writes.
on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:
engine:
  id: copilot
  model: gpt-4o
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
    run: |
      set -euo pipefail
      mkdir -p /tmp/gh-aw/agent
      SINCE=$(date -u -d '90 days ago' '+%Y-%m-%d')
      echo "Window start: $SINCE"

      gh api -X GET search/issues \
        -f q="org:adoptium is:pr is:merged merged:>=$SINCE" \
        -f per_page=100 --paginate \
        --jq '.items[] | {number, title, user: .user.login, repo: (.repository_url | sub("https://api.github.com/repos/"; "")), merged: .pull_request.merged_at}' \
        | jq -s '.' > /tmp/gh-aw/agent/merged-prs.json

      gh api -X GET search/issues \
        -f q="org:adoptium is:issue is:closed closed:>=$SINCE" \
        -f per_page=100 --paginate \
        --jq '.items[] | {number, title, user: .user.login, repo: (.repository_url | sub("https://api.github.com/repos/"; ""))}' \
        | jq -s '.' > /tmp/gh-aw/agent/closed-issues.json

      jq -n \
        --slurpfile prs /tmp/gh-aw/agent/merged-prs.json \
        --slurpfile iss /tmp/gh-aw/agent/closed-issues.json \
        '{
          window_start: "'"$SINCE"'",
          total_merged_prs: ($prs[0] | length),
          total_closed_issues: ($iss[0] | length),
          repos_touched: ([$prs[0][].repo] | unique | length),
          prs_by_repo: ([$prs[0][].repo] | group_by(.) | map({repo: .[0], count: length}) | sort_by(-.count)),
          contributors: ([$prs[0][].user] | group_by(.) | map({user: .[0], merged_prs: length}) | sort_by(-.merged_prs))
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
- `/tmp/gh-aw/agent/summary.json` — pre-computed aggregates: totals, PRs grouped by repository, and contributors ranked by merged-PR count. Read this first.
- `/tmp/gh-aw/agent/merged-prs.json` — the full list of merged PRs (number, title, author, repo) for detail in the highlights.
- `/tmp/gh-aw/agent/closed-issues.json` — closed issues over the window.

## Your task
Using only the files above, write a concise quarterly contribution impact report and create exactly one GitHub issue in this repository.

The contributors in `summary.json` are already ranked by merged-PR count. Treat that count as the base signal, but you may adjust the narrative ranking using PR titles in `merged-prs.json` where a contributor's work is clearly higher-impact. State your reasoning briefly.

## The issue must contain
- A header summary: window covered, total merged PRs, total closed issues, and number of distinct repositories touched.
- A ranked list of the top contributors by estimated impact, each with their merged-PR count and a one-line justification.
- A "Top 10 contributions" highlight section drawn from `merged-prs.json`, chosen for apparent impact based on titles.
- An "Activity by repository" section from `prs_by_repo`, listing the most active repositories.
- Suggested next steps or items needing maintainer attention for the next quarter.

## Constraints
- Create exactly one issue.
- Do not fetch any additional data; rank and summarize only what is on disk.
- Impact scoring is heuristic; flag anything that may warrant human review.
- Keep it concise and skimmable.