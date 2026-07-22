---
description: Translates updated Adoptium documentation files into a chosen language and creates GitHub issues with translated content for review.
on:
  workflow_dispatch:
    inputs:
      language:
        description: "Target language for translation."
        required: true
        type: choice
        options:
          - French
          - Spanish
          - German
          - Chinese
          - Japanese
          - Arabic
      file_path:
        description: "Specific file to translate (relative path, e.g. content/asciidoc-pages/docs/faq/index.adoc). Leave empty to translate all docs changed in the last 7 days."
        required: false
        type: string

engine:
  id: copilot

timeout-minutes: 45

permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write

network:
  allowed:
    - defaults

steps:
  - name: Fetch documentation files to translate
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      INPUT_LANGUAGE: ${{ inputs.language }}
      INPUT_FILE_PATH: ${{ inputs.file_path }}
    run: |
      set -euo pipefail
      mkdir -p /tmp/gh-aw/agent

      LANGUAGE="${INPUT_LANGUAGE}"
      FILE_PATH="${INPUT_FILE_PATH:-}"

      echo "Target language: $LANGUAGE"
      echo "Specific file: ${FILE_PATH:-none - will scan recently changed files}"

      gh repo clone adoptium/adoptium.net /tmp/gh-aw/adoptium-net -- --depth=50

      cd /tmp/gh-aw/adoptium-net

      if [ -n "$FILE_PATH" ]; then
        if [ ! -f "$FILE_PATH" ]; then
          echo "::error::File not found in adoptium/adoptium.net: $FILE_PATH"
          exit 1
        fi

        content=$(cat "$FILE_PATH")
        printf '%s' "$content" | jq -Rs --arg p "$FILE_PATH" '[{path: $p, content: .}]' \
          > /tmp/gh-aw/agent/docs-to-translate.json
      else
        git log --since="7 days ago" --name-only --pretty=format: \
          -- 'content/asciidoc-pages/**' 'content/blog/**' \
          | grep -E '\.(md|adoc)$' | sort -u \
          > /tmp/gh-aw/agent/changed-files.txt || true

        if [ ! -s /tmp/gh-aw/agent/changed-files.txt ]; then
          echo "No documentation files changed in the last 7 days."
          echo "[]" > /tmp/gh-aw/agent/docs-to-translate.json
        else
          echo "Files to translate:"
          cat /tmp/gh-aw/agent/changed-files.txt

          echo "[]" > /tmp/gh-aw/agent/docs-to-translate.json

          while IFS= read -r filepath; do
            if [ -f "$filepath" ]; then
              content=$(cat "$filepath")
              jq --arg p "$filepath" --arg c "$content" \
                '. += [{path: $p, content: $c}]' \
                /tmp/gh-aw/agent/docs-to-translate.json \
                > /tmp/gh-aw/agent/docs-tmp.json
              mv /tmp/gh-aw/agent/docs-tmp.json /tmp/gh-aw/agent/docs-to-translate.json
            fi
          done < /tmp/gh-aw/agent/changed-files.txt
        fi
      fi

      case "$LANGUAGE" in
        French)   CODE="fr" ;;
        Spanish)  CODE="es" ;;
        German)   CODE="de" ;;
        Chinese)  CODE="zh" ;;
        Japanese) CODE="ja" ;;
        Arabic)   CODE="ar" ;;
        *)        CODE="xx" ;;
      esac

      jq -n --arg lang "$LANGUAGE" --arg code "$CODE" \
        '{target_language: $lang, language_code: $code}' \
        > /tmp/gh-aw/agent/translation-config.json

      echo "=== Files queued for translation ==="
      jq '[.[] | {path, chars: (.content | length)}]' /tmp/gh-aw/agent/docs-to-translate.json

      echo "=== Translation config ==="
      cat /tmp/gh-aw/agent/translation-config.json

safe-outputs:
  create-issue:
    title-prefix: "[translation] "
    labels: [translation, documentation]
    max: 10
  add-comment:
    max: 50
    target: "*"
---

# Documentation Translation

Translate Adoptium documentation into the requested language and publish the translated content as GitHub issues for review.

## Pre-fetched data

The documentation files and config have already been fetched.

Read these files from disk:

- `/tmp/gh-aw/agent/docs-to-translate.json`
- `/tmp/gh-aw/agent/translation-config.json`

Each item in `docs-to-translate.json` has:

- `path`
- `content`

`translation-config.json` has:

- `target_language`
- `language_code`

Do not call shell commands or GitHub read tools to clone repositories or read source files. The source content is already available in the JSON files above.

Use only the safe-output tools when publishing results:

- `create_issue`
- `add_comment`
- `missing_data`
- `noop`

## Main task

1. Read `docs-to-translate.json`.
2. Read `translation-config.json`.
3. Translate each source file into the target language.
4. Create exactly one GitHub issue per translated source file.
5. Put Part 1 of the translation in the issue body using `create_issue`.
6. Put Part 2 and later in comments on the same issue using `add_comment`.
7. Do not create separate issues for Part 2, Part 3, etc.
8. Do not modify the original English source files.
9. Do not create commits or pull requests.
10. **IMPORTANT: Add a 2-3 second delay between each `add_comment` call to ensure proper ordering.**

## If there are no files to translate

If `docs-to-translate.json` is empty, create one issue explaining:

- no documentation files changed in the last 7 days
- the user can rerun the workflow with a specific `file_path`
- example: `content/asciidoc-pages/docs/faq/index.adoc`

Use a short title like:

```text
No documentation files to translate
```

## Translation rules

Preserve the source structure exactly.

- The translated file must mirror the original line by line.
- Every original line must have a corresponding translated line.
- Preserve blank lines.
- Preserve indentation.
- Preserve AsciiDoc and Markdown syntax.
- Preserve headings, list markers, tables, block delimiters, anchors, attributes, links, and frontmatter keys.
- Translate only human-readable prose.
- Do not translate code snippets.
- Do not translate variable names.
- Do not translate file paths.
- Do not translate URLs.
- Do not translate HTML tags.
- Do not translate AsciiDoc attribute names.
- Do not translate product names such as Eclipse Temurin, Adoptium, AQAvit, OpenJDK, JDK, JRE, JVM, GitHub, API, or Gradle unless the target language normally transliterates them.

## Output filename rule

Use the language code as a suffix before the file extension.

Examples:

```text
content/asciidoc-pages/docs/faq/index.adoc -> content/asciidoc-pages/docs/faq/index.ar.adoc
content/blog/example/index.md -> content/blog/example/index.fr.md
```

## Part sizing rule

Safe-output bodies must stay small.

For every issue body and every comment body:

- Keep the total body under 8,000 characters.
- Prefer chunks of at most 4,000 translated-content characters.
- Count headers, fenced-code markers, notes, and footer text in the total size.
- Split only at line boundaries.
- If unsure, split into smaller parts.

After splitting, calculate `N` as the total number of parts.

Use labels like (where N is the total number of parts):

```text
Part 1 of 3
Part 2 of 3
Part 3 of 3
```

Do not use `N = ceil(total characters / 60000)`. That is too large.

## Temporary ID rule

Use temporary IDs to connect comments to the issue created earlier.

For each source file, choose a short temporary ID:

```text
aw_file1
aw_file2
aw_faq1
aw_doc1
```

Temporary IDs must:

- start with `aw_`
- use only letters, numbers, and underscores
- be short: 3 to 12 characters after `aw_`
- not contain hyphens
- not contain long names such as `aw_issue_file1_part1`

Correct examples:

```text
aw_file1
aw_faq1
aw_doc2
```

Wrong examples:

```text
aw_issue_file1_part1
aw-file-1
file1
```

## Safe-output process for each translated file

### Step 1: Create the issue for Part 1

Call `create_issue` once for the file.

Use:

- `temporary_id`
- `title`
- `body`

The title should not include the `[translation]` prefix manually because the workflow adds it automatically.

Example:

```json
create_issue({
  "temporary_id": "aw_file1",
  "title": "content/asciidoc-pages/docs/faq/index.adoc -> Arabic (Part 1 of 3)",
  "body": "ISSUE BODY HERE"
})
```

### Step 2: Add later parts as comments

For Part 2 and later, call `add_comment`.

Set `item_number` to the same temporary ID used in `create_issue`.

**CRITICAL: After each `add_comment` call, wait 2-3 seconds before posting the next comment. This ensures GitHub processes comments in the correct order.**

Example flow:

```json
add_comment({
  "item_number": "aw_file1",
  "body": "**Part:** Part 2 of 4\n\n...(COMMENT BODY HERE)..."
})
// WAIT 2-3 SECONDS

add_comment({
  "item_number": "aw_file1",
  "body": "**Part:** Part 3 of 4\n\n...(COMMENT BODY HERE)..."
})
// WAIT 2-3 SECONDS

add_comment({
  "item_number": "aw_file1",
  "body": "**Part:** Part 4 of 4\n\n...(COMMENT BODY HERE)..."
})
```

Do not guess issue numbers.

Do not use issue numbers like `1`, `17`, or `18`.

Do not use bash to extract issue numbers.

Do not parse response text from `create_issue`.

The safe-output system resolves the temporary ID automatically.

## Issue body template

Use this structure for Part 1:

````markdown
**File:** `SOURCE_PATH`
**Target language:** TARGET_LANGUAGE
**Part:** Part 1 of N
**Suggested output filename:** `OUTPUT_PATH`

```adoc
TRANSLATED_CONTENT_CHUNK_1
```

**Notes for human review:**

- Review technical terminology and idioms.
- Confirm formatting still renders correctly.

This translation was AI-generated and should be reviewed by a native speaker before being committed.
````

For Markdown files, use:

````markdown
```markdown
TRANSLATED_CONTENT_CHUNK
```
````

For AsciiDoc files, use:

````markdown
```adoc
TRANSLATED_CONTENT_CHUNK
```
````

## Comment body template

Use this structure for Part 2 and later:

````markdown
**Part:** Part X of N

```adoc
TRANSLATED_CONTENT_CHUNK_X
```

**Notes for human review:**

- Review technical terminology and idioms.
- Confirm formatting still renders correctly.
````

For the final part, also include:

```text
This translation was AI-generated and should be reviewed by a native speaker before being committed.
```

## Critical constraints

- Exactly one issue per source file.
- Part 1 goes in the issue body.
- Part 2 and later go in comments on that same issue.
- Use `temporary_id` on `create_issue`.
- Use that same temporary ID as `item_number` on `add_comment`.
- Never create separate issues for later parts.
- Never call `missing_tool` because the translation is too large.
- If the output is too large, split it into smaller parts.
- Keep every issue body and comment body under 8,000 characters.
- Preserve source structure line by line.
- Do not fetch additional documentation.
- Do not create pull requests.
- Do not commit files.
- **Add a 2-3 second delay between each `add_comment` call to ensure proper comment ordering on GitHub.**
