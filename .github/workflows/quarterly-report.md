---
description: Generates a quarterly contribution impact report ranked by estimated positive impact, posted as a GitHub issue.
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
1. Enumerate **all** public repositories in the `adoptium` organization. Use pagination (fetch up to 100 repositories per page and continue fetching subsequent pages) until all repositories have been collected before proceeding. Do not stop after the first page of results.
2. **Pre-filter before deep data collection**: for each repository, first check `pushed_at` (or equivalent last-activity timestamp). Skip detailed commit/PR/issue/review collection for repositories with no activity in the last 90 days — record them as inactive and move on. This avoids spending request budget on repositories that will contribute nothing to the report.
3. For each remaining (active) repository, collect commits, pull requests, issues closed, and code reviews submitted in the last 90 days. Process repositories in small batches (e.g., 5-10 at a time) rather than issuing every request for every repository at once, and prefer fetching only the fields needed for scoring (e.g., title, author, merged/closed date, additions/deletions) rather than full object payloads.
4. If a data-fetch call for a given repository times out or errors after one retry, skip that repository's remaining data for this run, note it in a "Repositories with incomplete data" section of the report, and continue with the rest. A partial report covering most of the org is preferable to a full failure.
5. Classify each contribution by type (bug fix, feature, refactor, docs, etc.) and score by estimated impact.
6. Aggregate into one concise ranked report and create a single GitHub issue in this repository.

## Constraints
- Keep the report concise and skimmable; prioritize signal over volume.
- Create exactly one issue, even if some repositories had incomplete data (see Process step 4).
- Exclude bot contributors (e.g., dependabot).
- Impact scoring is heuristic-based; flag contributions that may warrant human review. Not meant to be exhaustive.
