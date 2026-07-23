# Committer Support: Agentic Workflows

This document summarises the AI-powered (Copilot) agentic workflows defined in this repository. Each workflow runs autonomously on a schedule or on demand, gathering data deterministically before handing off to the agent for analysis and writing.

---

## Weekly Org Status Report

**Workflow file:** `.github/workflows/repo-status.md`  
**Trigger:** Weekly (every Monday at 09:00 UTC); manual dispatch also available.

### What it does

Scans all public repositories in the `adoptium` GitHub organisation for activity in the previous seven days. It enumerates repositories, gathers recent issues, pull requests, commits and releases, and then produces a single concise status report with org-level highlights and suggested maintainer actions.

### Output

Creates one GitHub issue in this repository labelled `report` and `weekly-status` with the title prefix `[adoptium-status]`. Any issue from a previous week's run is automatically closed when the new one is created.

### Suggested use

Review the issue each Monday to get a quick pulse on org-wide activity. Use the "items needing maintainer attention" section to triage cross-project work and spot repositories that may need help.

---

## Quarterly Issue Burn-down Report

**Workflow file:** `.github/workflows/issue-burn-down.md`  
**Trigger:** Quarterly (1st day of each quarter at 09:00 UTC); manual dispatch also available.

### What it does

Fetches all issues opened and closed across the `adoptium` organisation during the previous calendar quarter. It computes per-repository open/close/burn-down scores and identifies stale issues (open for more than 30 days without activity) and under-served labels (labels where open issues consistently outpace closed ones).

### Output

Creates one GitHub issue in this repository labelled `report` and `burndown` with the title prefix `[burndown]`. Any issue from a previous quarter's run is automatically closed when the new one is created.

### Suggested use

Use the burn-down report at the start of each quarter to understand which repositories are accumulating unresolved issues, which labels represent chronic under-investment, and which specific stale issues should be prioritised or closed.

---

## Quarterly Contribution Impact Report

**Workflow file:** `.github/workflows/quarterly-report-deterministic.md`  
**Trigger:** Quarterly (1st day of each quarter at 09:00 UTC); manual dispatch with optional custom date range.

### What it does

Gathers all merged pull requests and closed issues across the `adoptium` organisation over the previous quarter (or a custom window). It ranks contributors by estimated impact, highlights notable pull requests and the most active repositories, and reports Copilot-assisted contributions alongside the humans who guided them.

### Output

Creates one GitHub issue in this repository labelled `report` and `quarterly-impact` with the title prefix `[quarterly-impact]`.

### Suggested use

Share the report in PMC meetings or working-group updates as a summary of progress and community health. Use the contributor rankings and Copilot-assistance data when recognising contributors or when preparing release notes and retrospectives.

---

## Periodic FAQ Review

**Workflow file:** `.github/workflows/periodic-faq.md`  
**Trigger:** Weekly; manual dispatch also available.

### What it does

Reviews community questions from multiple channels — `adoptium/adoptium-support` issues, GitHub Discussions, Stack Overflow (Adoptium / Temurin / AdoptOpenJDK tags), Reddit mentions, the PMC mailing list archive, and the Slack workspace — and compares them against the live [Adoptium FAQ](https://adoptium.net/docs/faq/). It clusters recurring questions, identifies gaps in the FAQ, and proposes ready-to-apply additions or revisions.

### Output

Creates one GitHub issue in this repository labelled `documentation` and `faq` with the title prefix `[faq-review]`. Issues are not automatically closed (they persist for human review).

### Suggested use

Assign the issue to a documentation maintainer for review. Approved proposals can be applied directly to the FAQ source in `adoptium/adoptium.net`. Recurring themes across multiple runs signal high-priority documentation gaps.

---

## Release Blog Draft

**Workflow file:** `.github/workflows/release-blog-draft.md`  
**Trigger:** Manual dispatch only. Requires specifying the release type (`cpu`, `cspu`, or `feature`), the JDK versions included, an optional content-issue number from `adoptium/adoptium.net`, and an optional start date for the release window.

### What it does

Gathers release-tracking issues from `adoptium/temurin`, the release plan from `adoptium/mirror-scripts`, merged pull requests from the delivery repositories (`temurin-build`, `installer`, `containers`) since the release window start, and recent published blog posts as format examples. Using this material it drafts a complete, review-ready Adoptium release blog post in the format used by `adoptium.net`.

### Output

Creates one GitHub issue in this repository labelled `release`, `blog`, `draft`, and `automation` with the title prefix `[release-blog]`. The issue body contains the full draft blog post, ready for editorial review. The workflow produces no direct file commits; a human must copy the approved content into `adoptium/adoptium.net`.

### Suggested use

Trigger this workflow one to two days before the planned release announcement. Review the created issue for accuracy (version numbers, platform availability, security-fix descriptions) against the official release checklist, fill in any sections flagged as needing human input, then publish the finalised post to `adoptium/adoptium.net`.

---

## Documentation Translation

**Workflow file:** `.github/workflows/translation-2.md`  
**Trigger:** Manual dispatch only. Requires selecting a target language (French, Spanish, German, Chinese, Japanese, or Arabic) and optionally specifying a single file path. When no file is given, all documentation files changed in the last seven days are translated.

### What it does

Fetches the specified Adoptium documentation source files from `adoptium/adoptium.net` and translates them into the requested language. Each translated document is filed as a separate GitHub issue for review before it is published.

### Output

Creates up to 10 GitHub issues in this repository (one per translated file) labelled `translation` and `documentation` with the title prefix `[translation]`. If multiple files are translated, a follow-up comment is added to each issue referencing the related translations.

### Suggested use

Run this workflow when documentation has been updated and localised versions need refreshing, or when onboarding a new language community. Assign the resulting issues to bilingual reviewers or native-speaker contributors before merging the translated content into `adoptium/adoptium.net`.
