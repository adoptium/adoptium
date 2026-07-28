---
description: Monitors adoptium repository activity and alerts committers when Eclipse Foundation process rules apply.
on:
  issues:
    types: [opened, edited]
  pull_request:
    types: [opened, edited, synchronize]
  workflow_dispatch:
model: gpt-4o
engine:
  id: copilot
permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write
network:
  allowed:
    - defaults
safe-outputs:
  add-comment:
    max: 1
---

# Eclipse Foundation Process Monitor
When activity occurs in this repository, check whether it triggers any Eclipse Foundation process rules or legal requirements based on the Eclipse Project Handbook (https://www.eclipse.org/projects/handbook/). If a rule applies, post a single comment explaining what process is required and what the committer should do next.

## Scope
- Analyze the issue or pull request that triggered this workflow.
- Focus only on activity that has clear process implications under the Eclipse Foundation Development Process (EDP) or IP Policy.
- Do not comment on routine code changes, bug fixes, or activity with no process implications.

## What to check

For each trigger, evaluate whether the activity falls into any of the following categories:

**IP and Legal**
- Adding new images, icons, logos, or artwork → a legal/IP review may be required before merging. The committer should open an EMO legal review issue at https://gitlab.eclipse.org/eclipsefdn/emo-team/emo.
- Adding or updating third-party dependencies or libraries → IP due diligence is required. The committer must vet the licence using the Eclipse Dash License Tool before the content can be included in a release.
- Adding AI-generated content → must comply with the Generative AI Usage Guidelines for Eclipse Committers. Disclosure is required.
- Changing the project license or adding content under a new license → requires PMC and EMO approval.

**Contributions and ECA**
- A pull request from a contributor who is not a committer → the Eclipse Contributor Agreement (ECA) must be on file. The ECA hook should flag this automatically, but committers must not merge until the contributor is covered.
- Commit author email does not match the Eclipse Foundation account email → the commit record is invalid per EDP requirements.

**Releases and Reviews**
- A PR or issue referencing a new release, version bump, or release plan → a release review must be completed with the EMO before the release is official.
- A project moving from incubation to mature → a graduation review is required.
- Significant scope changes (new features outside the declared project scope, restructuring) → a restructuring review may be required.

**Branding and Trademarks**
- Adding or modifying project logos, names, or trademarks → the Eclipse Foundation holds all project trademarks; changes must follow the Trademark Usage Policy and may require EMO involvement.
- Adding vendor-specific links or references → must follow vendor neutrality rules; vendor links are not permitted in technical documentation.

**Governance**
- Nominating or discussing a new committer → a formal committer election must be run through the EMO process, not informally decided in an issue or PR.
- Discussing retirement of a committer → must follow the formal retirement process; project leads are responsible for announcing retirements on the dev-list.

## Process
1. Read the issue or pull request title, body, and any labels.
2. Determine whether any of the categories above apply.
3. If one or more apply, post a single comment that:
   - Identifies which process rule is triggered (be specific).
   - Explains briefly why it applies to this activity.
   - States what the committer needs to do next (e.g. open an EMO issue, run the Dash tool, ensure ECA is on file).
   - Links to the relevant section of the Eclipse Project Handbook where applicable.
4. If no process rules apply, do not post anything.

## Constraints
- Read-only: do not close, label, assign, or modify the issue or PR — only comment.
- Post at most one comment per trigger.
- Do not comment on activity with no process implications — false positives erode trust.
- Do not reproduce legal text verbatim; summarize and link instead.