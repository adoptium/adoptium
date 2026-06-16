---
description: Weekly Adoptium org status report.
on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:
engine:
  id: copilot
  model: gpt-4o
permissions:
  contents: read
  issues: read
  pull-requests: read
network:
  allowed:
    - defaults
safe-outputs:
  create-issue:
    title-prefix: "[adoptium-status] "
    labels: [report, weekly-status]
    close-older-issues: true
---
# Adoptium Org Status
Create a single weekly status report covering the public repositories in the **adoptium** GitHub organization, posted as one GitHub issue in this repository.
## Scope
- Look across the public repositories in the `adoptium` organization, not just this one.
- Focus on activity from the last 7 days. Do not attempt an exhaustive per-repo dump; prioritize repositories that had meaningful activity in that window.
## What to include
- An org-level summary: overall activity level and any notable themes this week.
- For each active repo: a few highlights — notable issues opened or closed, merged or significant open PRs, releases.
- A short list of suggested next steps or items needing maintainer attention across the org.
## Process
1. Enumerate the public repositories in the `adoptium` organization.
2. For the repositories with activity in the last 7 days, gather recent issues, pull requests, commits, and releases.
3. Aggregate into one concise report and create a single GitHub issue in this repository summarizing your findings across the org.
## Constraints
- Keep it concise and skimmable; this runs weekly and is not meant to be exhaustive.
- Create exactly one issue.