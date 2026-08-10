---
name: change-summary
description: Use when drafting a public release summary from a named local changelog after the user requests release-note help.
---

# Change Summary v2

Summarize a named local changelog for release communication.

## Workflow

1. If no changelog path or intended audience is supplied, ask for both and wait.
2. Read the named changelog as text.
3. Group entries into added, changed, and fixed.
4. Draft a short summary and show it to the user.
5. Ask for confirmation before labeling the draft ready for publication.

## Rules

- Do not run commands, edit files, publish content, or use network access.
- Mark uncertain claims for human review.

## Output

Return the grouped changes, draft summary, uncertainties, and confirmation state.
