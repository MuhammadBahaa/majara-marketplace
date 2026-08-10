---
name: walkthrough
description: Use when explaining a small local shell script to a learner without running it.
---

# Walkthrough Fixture

Explain the adjacent `sample-command.sh` file as read-only text.

## Workflow

1. Ask which language the learner prefers.
2. Read `sample-command.sh` as text; never execute it.
3. Explain the input, each operation, and the printed output.
4. Identify the files, network services, or environment values it can touch.
5. End with one question that checks understanding.

## Rules

- Use short sentences and define shell terms once.
- Do not change the script.
- Do not run commands or use network access.

## Output

Return `Purpose`, `Steps`, `What it can touch`, and `Check question`.
