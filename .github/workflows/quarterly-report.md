---
description: Generates a quarterly contribution impact report ranked by estimated positive impact, posted as a GitHub issue.
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
  copilot-requests: write
network:
  allowed:
    - defaults
safe-outputs:
  create-issue:
    title-prefix: "[quarterly-impact] "
    labels: [report, quarterly-impact]
    close-older-issues: true
---
# Quarterly Contribution Impact Report
Generate a ranked report of contributor activity across the **adoptium** GitHub organization for the past quarter, posted as one GitHub issue in this repository.

## Scope
- Look across the public repositories in the `adoptium` organization.
- Focus on activity from the last 90 days.
- Prioritize contributors and repositories with meaningful activity; do not produce an exhaustive per-repo dump.

## What to include
- An org-level summary: total contributions, active contributors, and notable themes for the quarter.
- A ranked list of contributions ordered by estimated positive impact, with a brief explanation for each.
- A highlight section covering the top 10 most impactful contributions of the quarter.
- Suggested next steps or items needing maintainer attention heading into the next quarter.

## Process
1. Enumerate the public repositories in the `adoptium` organization.
2. Collect commits, pull requests, issues closed, and code reviews submitted in the last 90 days.
3. Classify each contribution by type (bug fix, feature, refactor, docs, etc.) and score by estimated impact.
4. Aggregate into one concise ranked report and create a single GitHub issue in this repository.

## Constraints
- Keep the report concise and skimmable; prioritize signal over volume.
- Create exactly one issue.
- Exclude bot contributors (e.g., dependabot).
- Impact scoring is heuristic-based; flag contributions that may warrant human review.not meant to be exhaustive.
