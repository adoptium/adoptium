---
name: Release Blog Draft
description: Drafts an Adoptium release blog post near the end of a release period. Release content, temurin release-summary issues, delivery-repo activity, and recent example posts are gathered deterministically; the agent only assesses and writes the draft, filing it as an issue for a human to review.
on:
  workflow_dispatch:
    inputs:
      release_type:
        description: "Release type: cpu (quarterly Critical Patch Update), cspu (Critical Security Patch Update), or feature (new JDK version)."
        required: true
        type: choice
        options:
          - cpu
          - cspu
          - feature
      jdk_versions:
        description: "JDK versions in this release, comma-separated. Example: 8, 11, 17, 21, 25"
        required: true
        type: string
      content_issue:
        description: "Issue number in adoptium/adoptium.net holding the human-collected release content (e.g. 1053). Optional."
        required: false
        type: string
      since:
        description: "Start of the release window (YYYY-MM-DD) for scanning delivery-repo activity. Defaults to the date of the last GA tag of the first listed JDK version (i.e. since that version last released), falling back to 90 days ago."
        required: false
        type: string

engine:
  id: copilot

timeout-minutes: 20

permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write

network:
  allowed:
    - defaults
    - github

# All GitHub data is fetched deterministically before the agent runs. This keeps
# the run cheap and reproducible: the agent reads files and writes prose, it does
# not go spelunking through the API itself. Every fetch targets public adoptium
# repositories and tolerates empty results rather than failing the run.
steps:
  - name: Gather release inputs
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      INPUT_RELEASE_TYPE: ${{ inputs.release_type }}
      INPUT_JDK_VERSIONS: ${{ inputs.jdk_versions }}
      INPUT_CONTENT_ISSUE: ${{ inputs.content_issue }}
      INPUT_SINCE: ${{ inputs.since }}
    run: |
      set -euo pipefail
      AGENT_DIR=/tmp/gh-aw/agent
      mkdir -p "$AGENT_DIR/example-posts"

      # A tiny retry wrapper: GitHub search occasionally returns an empty 200.
      gh_retry() { # $@ = gh api args; prints stdout, empty string on repeated failure
        local attempt
        for attempt in 1 2 3; do
          if OUT=$(gh api "$@" 2>/dev/null); then printf '%s' "$OUT"; return 0; fi
          sleep 5
        done
        printf ''
        return 0
      }

      # Default the release window to "since this version last released": the
      # date of the most recent GA tag (e.g. jdk-21.0.11-ga, jdk8u492-ga) in the
      # mirror repo of the first listed JDK version. Fall back to 90 days.
      SINCE="${INPUT_SINCE:-}"
      if [ -z "$SINCE" ]; then
        FIRST_V=$(echo "$INPUT_JDK_VERSIONS" | cut -d, -f1 | tr -d '[:space:]')
        MIRROR="jdk${FIRST_V}u"
        # Walk GA tags newest-first and take the first one older than 21 days:
        # right around a release the newest GA tag is the release being drafted,
        # and the window should reach back to the *previous* one.
        CUTOFF=$(date -u -d '21 days ago' '+%Y-%m-%d')
        for GA_TAG in $(gh_retry "repos/adoptium/$MIRROR/tags?per_page=100" \
            --jq '.[].name' | grep -- '-ga$' | grep -v dryrun | sort -rV | head -4); do
          TAG_DATE=$(gh_retry "repos/adoptium/$MIRROR/commits/$GA_TAG" \
            --jq '.commit.committer.date' | cut -dT -f1)
          [ -n "$TAG_DATE" ] || continue
          if [ "$TAG_DATE" \< "$CUTOFF" ]; then
            SINCE=$TAG_DATE
            echo "Last released GA tag of JDK $FIRST_V: $GA_TAG ($SINCE)"
            break
          fi
        done
      fi
      [ -n "$SINCE" ] || SINCE=$(date -u -d '90 days ago' '+%Y-%m-%d')
      echo "$SINCE" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' \
        || { echo "::error::Invalid since date '$SINCE' (expected YYYY-MM-DD)"; exit 1; }
      echo "Release type: ${INPUT_RELEASE_TYPE}"
      echo "JDK versions: ${INPUT_JDK_VERSIONS}"
      echo "Scanning delivery-repo activity since: $SINCE"

      # 1. Human-collected content issue (optional).
      if [ -n "${INPUT_CONTENT_ISSUE:-}" ]; then
        echo "Fetching adoptium/adoptium.net#${INPUT_CONTENT_ISSUE}"
        {
          gh_retry "repos/adoptium/adoptium.net/issues/${INPUT_CONTENT_ISSUE}" \
            --jq '"# " + .title + "\n\n" + (.body // "")'
          echo
          echo "## Comments"
          echo
          gh_retry "repos/adoptium/adoptium.net/issues/${INPUT_CONTENT_ISSUE}/comments" \
            --jq '.[] | "### @" + .user.login + "\n\n" + (.body // "") + "\n"'
        } > "$AGENT_DIR/content-issue.md" || true
      else
        echo "No content_issue provided." > "$AGENT_DIR/content-issue.md"
      fi

      # 2. Release-tracking issues in adoptium/temurin, updated within the window.
      #    The team does not use a "release summary" title; the useful trackers are
      #    the release checklist, the per-platform release status matrix, and the
      #    release retrospective. Match those title conventions.
      gh_retry -X GET search/issues \
        -f q="repo:adoptium/temurin in:title (\"Release Status\" OR \"Checklist for Temurin Release\" OR \"Retrospective\") updated:>=$SINCE" \
        -f per_page=30 \
        --jq '[.items[] | {number, title, state, url: .html_url, updated: .updated_at, body: (.body // "" | .[0:12000])}]' \
        > "$AGENT_DIR/release-summaries.json"
      [ -s "$AGENT_DIR/release-summaries.json" ] || echo '[]' > "$AGENT_DIR/release-summaries.json"

      # 2b. The release plan from adoptium/mirror-scripts: its GA tags (e.g.
      #     jdk-26.0.2-ga) pin the exact upstream tags/SHAs for each version in
      #     the release, letting the agent derive full version+build strings.
      gh_retry "repos/adoptium/mirror-scripts/contents/releasePlan.cfg" \
        --jq '.content' | base64 -d > "$AGENT_DIR/releasePlan.cfg" 2>/dev/null || true
      [ -s "$AGENT_DIR/releasePlan.cfg" ] || echo "unavailable" > "$AGENT_DIR/releasePlan.cfg"

      # 3. Notable delivery changes: merged PRs since the window in the delivery repos.
      : > "$AGENT_DIR/repo-activity.json"
      echo '{}' > "$AGENT_DIR/repo-activity.json"
      TMP_ACT=$(mktemp)
      echo '{}' > "$TMP_ACT"
      for repo in temurin-build installer containers; do
        PRS=$(gh_retry -X GET search/issues \
          -f q="repo:adoptium/$repo is:pr is:merged merged:>=$SINCE" \
          -f per_page=50 \
          --jq '[.items[] | {number, title, url: .html_url, merged: .pull_request.merged_at}]')
        [ -n "$PRS" ] || PRS='[]'
        jq --arg r "$repo" --argjson prs "$PRS" '. + {($r): $prs}' "$TMP_ACT" > "$TMP_ACT.next" \
          && mv "$TMP_ACT.next" "$TMP_ACT"
      done
      mv "$TMP_ACT" "$AGENT_DIR/repo-activity.json"

      # 4. Recent published release posts, as house-style references. The site
      #    keeps posts at content/blog/<slug>/index.md; release announcements use
      #    slugs ending in "-available". Grab the latest CPU-update post (the
      #    "eclipse-temurin-8u..." series sorts chronologically by name) and the
      #    latest feature-release post ("eclipse-temurin-NN-available").
      DIRS=$(gh_retry "repos/adoptium/adoptium.net/contents/content/blog" \
        --jq '[.[] | select(.type == "dir") | .name]')
      [ -n "$DIRS" ] || DIRS='[]'
      CPU_POST=$(echo "$DIRS" | jq -r '.[]' | grep -E '^eclipse-temurin-8u.*-available$' | sort | tail -1 || true)
      FEATURE_POST=$(echo "$DIRS" | jq -r '.[]' | grep -E '^eclipse-temurin-[0-9]+-available$' | sort -V | tail -1 || true)
      for slug in $CPU_POST $FEATURE_POST; do
        echo "Fetching example post: $slug"
        gh_retry "repos/adoptium/adoptium.net/contents/content/blog/${slug}/index.md" \
          --jq '.content' | base64 -d > "$AGENT_DIR/example-posts/${slug}.md" 2>/dev/null || true
      done
      ls -la "$AGENT_DIR/example-posts" || true

      echo "=== Gathered files ==="
      ls -la "$AGENT_DIR"

safe-outputs:
  allowed-domains:
    - adoptium.net
    - hub.docker.com
    - github.com
  noop:
    report-as-issue: false
  create-issue:
    title-prefix: "[release-blog] "
    labels: [release, blog, draft, automation]
---

# Release Blog Draft

All the source material for this release has already been gathered for you before this step ran. Do NOT call GitHub tools or shell commands to fetch more data — everything you need is on disk under `/tmp/gh-aw/agent/`. Your job is to assess what is notable and write a single, review-ready draft of the release blog post, then file it as an issue.

## What this release is

The person who started this run provided:

- **Release type**: read it from the workflow inputs echoed in the setup step. `cpu` means a quarterly Critical Patch Update that ships across all supported JDK versions (January, April, July, October). `cspu` means a Critical Security Patch Update, an out-of-band release containing only security patches; it may cover one or more versions depending on the patches delivered, and its versions use an extra dotted component (e.g. `26.0.2.1`). `feature` means a new JDK feature version (around March and April). The framing, headline, and emphasis differ: a CPU post leads with security and the set of updated versions; a CSPU post leads with the security fixes being delivered and states plainly that it is a security-only update to the affected version(s) — still scan the repo activity for other notable changes, but expect few; a feature post leads with what is new in the new JDK version.
- **JDK versions**: the comma-separated list of versions in this release.

## Pre-gathered material

- `/tmp/gh-aw/agent/content-issue.md` — the human-collected content from the `adoptium/adoptium.net` issue for this release, if a `content_issue` was provided. This is the **primary source of truth** for the narrative when present. If it says "No content_issue provided", rely on the other files and clearly flag where human input is still needed.
- `/tmp/gh-aw/agent/release-summaries.json` — release-tracking issues from `adoptium/temurin` updated during the release window: the release checklist, the per-platform release status matrix, and the release retrospective. Use these to confirm which versions and platforms are being delivered and to catch any release-specific notes.
- `/tmp/gh-aw/agent/releasePlan.cfg` — the release plan from `adoptium/mirror-scripts`. Its GA tags name the exact upstream version for each JDK in the release (e.g. `jdk-26.0.2-ga` corresponds to the `jdk-26.0.2+10` build tag; the two tags share a SHA in the version's mirror repo such as `adoptium/jdk26u`).
- `/tmp/gh-aw/agent/repo-activity.json` — merged pull requests since the window start in the delivery repositories (`temurin-build`, `installer`, `containers`), keyed by repository. Use these to identify notable changes in how binaries, installers, and containers are built and delivered. Summarize themes; do not list every PR.
- `/tmp/gh-aw/agent/example-posts/` — the most recent published CPU-update and feature-release posts from `adoptium.net`. **These are the format authority.** If they differ from the template below, follow the examples.

## Output structure and format

Adoptium release posts live at `content/blog/<slug>/index.md` in `adoptium/adoptium.net`, where the slug ends in `-available` (e.g. `eclipse-temurin-8u492-11031-17019-21011-2503-2601-available`, `eclipse-temurin-26-available`). Every post has this shape:

```markdown
---
title: Eclipse Temurin <versions> Available
date: "YYYY-MM-DD"
author: pmc
description: Adoptium is happy to announce the immediate availability of Eclipse Temurin <versions>. As always, all binaries are thoroughly tested and available free of charge without usage restrictions on a wide range of platforms.
tags:
  - temurin
  - announcement
  - release-notes
---

<Opening paragraph: the description sentence again, but with full version strings
including build numbers (e.g. 8u492-b09, 21.0.11+10), followed by the standard
links to the Temurin download page, DockerHub container images, and installable
packages.>

## Fixes and Updates

This release contains the following fixes and updates.

- [Temurin <version> release notes](https://adoptium.net/temurin/release-notes/?version=<tag>)
<one bullet per JDK version in the release>

## New and Noteworthy

### <Change headline in title case>

<Prose explaining the change from a user's perspective: what changed, why, and
what action (if any) they must take. Use bold for calls to action, code spans
for tags/package names, and bullet lists for platform/architecture coverage.>

<repeat one ### subsection per notable change>
```

- **Title**: CPU posts list every version, comma-separated with a final "and" (`Eclipse Temurin 8u492, 11.0.31, 17.0.19, 21.0.11, 25.0.3 and 26.0.1 Available`); feature posts are just `Eclipse Temurin <NN> Available`.
- **Author** is the literal string `pmc` (the site maps it to "Adoptium PMC") unless the content issue names someone else.
- Feature posts typically close with the standing **Contributing To Eclipse Temurin** and **Become An Eclipse Temurin Sustainer** sections — copy those from the feature example post verbatim.
- Full version strings with build numbers only appear in the body, not the title or description. Derive them from the gathered material: the `Release status per Platform, Version & Binary Type` issue in `release-summaries.json` lists the exact version+build strings (e.g. `21.0.11+10`, `8u492-b09`), and `releasePlan.cfg` cross-confirms them via the GA tags. Only flag a build number as a needs-human-input gap if neither source has it.
- **Release-notes links** use the exact form `https://adoptium.net/temurin/release-notes?version=jdk-25.0.3+9` (JDK 8 uses `jdk8u492-b09` style). These pages go live after publication, so keep the links even though they may 404 while drafting.

## Your task

1. Read the example posts first and confirm the structure above still matches. Read the content issue next, then the release summaries and repo activity.

2. Write a complete release blog post draft in that exact format:
   - The `New and Noteworthy` subsections are where the release-specific value lives. Source them from the content issue first, then from themes in the repo activity (new platforms, installer or container improvements, build changes) — plain language a user would care about, not a raw PR list.
   - State clearly which JDK versions and platforms are delivered.

3. Do not invent facts. Where the gathered material is silent on something a post would normally state (exact CVE list, release date, specific version strings), insert a short blockquote marker `> [!NOTE] Needs human input: <what is missing>` rather than guessing. It is better to hand a reviewer an honest gap than a confident error.

4. File the draft by calling the `create_issue` safe-output tool exactly once. The issue title should name the release, for example `Draft: July 2026 CPU release blog post (JDK 8, 11, 17, 21)`. The issue body is the full draft, including its frontmatter, inside a fenced code block so a reviewer can copy it verbatim. Above the code block, state the suggested file path (`content/blog/<slug>/index.md` with a slug following the `-available` convention), a one-paragraph summary of what you based the draft on, and a bullet list of every `Needs human input` gap you flagged.

## When there is nothing to write

If every gathered file is empty — no content issue, no release summaries, and no repo activity — there is not enough material to draft a post. In that case call `noop` with a short explanation of what was missing instead of creating an issue. Your chat response is not the deliverable; the draft only exists if you call `create_issue` (or `noop`).
