---
description: Daily repo status report.
on:
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
    title-prefix: "[repo-status] "
    labels: [report, daily-status]
---

# Repo Status

Create a brief daily status report for this repository as a GitHub issue.

## What to include
- Recent repository activity (issues, PRs, commits, releases)
- Project status and a few highlights
- A short list of suggested next steps for maintainers

## Process
1. Gather recent activity from the repository.
2. Review the open issues and pull requests.
3. Create a single GitHub issue summarizing your findings.