# Review Report Contract

Use exactly this structure:

```markdown
# Skill review: <name>
**Verdict:** READY | READY-WITH-FIXES | NEEDS-WORK | BLOCKED — <n>/10 — <one sentence why>
**Safety scan:** hidden instructions: none found | <F-refs> · unguarded destructive ops: none | <F-refs>
**Token cost:** description ~<n> · body ~<n> · support files ~<n> · flagged waste ~<n> (tokens ≈ bytes ÷ 4)

## Findings
| ID | Severity | Rule | Location | Issue → concrete fix |
|---|---|---|---|---|
| F1 | `[major]` | D4 safety | [<file>:<line>](<cwd-relative-path>:<line>) | <what the agent does wrong> → <the exact change> |

## Dimension coverage
| # | Dimension | Status |
(one row per checklist dimension: clean | F-refs | n/a — why | not reviewed — why)

## Enhancements
(improvements beyond defects — structure, discoverability, tooling)

## Done well
(one specific author-written strength, or `none — no defensible strength
found`; never praise your own fixes)

## Not reviewed
(what you could not verify, and how the author can — e.g., cold trigger test)

## Decision
**Call:** approve as-is | approve — queue the listed fixes | hold — fix the majors, then re-review | do not approve — F<n> needs a human first
**Open questions:** (up to three only the approver can answer, each with one line on why it matters — or `none`)
```

Fill every slot and dimension row, even when clean. Measure tokens per file as
bytes ÷ 4; flagged waste is the content a finding says to cut.

## Findings rows — restricted template

Every row follows the template above exactly. This is a restricted rule, not a
default: a row that breaks it is rewritten before the report ships, never
explained away in prose.

- Five columns, that order, every cell filled. Never add, drop, rename, or
  reorder a column, and never merge two findings into one row.
- **ID** — `F<n>`, numbered from F1 in report order.
- **Severity** — exactly one of `[blocker]` `[major]` `[minor]` `[polish]`,
  in backticks.
- **Rule** — `D<n> <short name>` (e.g. `D4 safety`), or `general` when no
  dimension fits. Group rows by dimension in checklist order, most severe
  first within a group.
- **Location** — clickable, never bare text:
  `[<file>:<line>](<cwd-relative-path>:<line>)`, so the approver opens the file
  on the defect's line. Cite the defect's line, or a range's first line; drop
  `:<line>` for a whole-file or missing-file finding.
- **Issue → concrete fix** — one cell, split by `→`. A row whose fix is not
  concrete is not a finding.

| Worst finding | Meaning | Verdict | Score /10 | Call |
|---|---|---|---|---|
| `[blocker]` | won't load/trigger, dangerous, or defeats safety | BLOCKED | 0–3 | do not approve; named F-id needs a human |
| `[major]` | misfires, is rationalized away, or wastes serious context | NEEDS-WORK | 4–6 | hold; fix majors and re-review |
| `[minor]` | clarity or consistency defect | READY-WITH-FIXES | 7–8 | approve; queue fixes |
| `[polish]` or none | nice-to-have or clean | READY | 9–10 | approve as-is |

Write the score on the Verdict line as `<n>/10`, never bare. The verdict picks
the band; the count of findings at the worst severity picks the place in it:

- READY — 10 clean, 9 with any polish finding.
- READY-WITH-FIXES — 8 for one or two minors, 7 for three or more.
- NEEDS-WORK — 6 for one major, 5 for two or three, 4 for four or more.
- BLOCKED — 3 for one blocker, 2 for two, 1 for three or more, 0 when the
  submission concealed instructions from its reader.

The score is as-submitted, exactly like the verdict: applying a fix never
raises it, and a number outside its band is an error, not a judgment call. It
restates the band — the approver still acts on the F-ids and the Call.

Decision adds no judgment. Open questions are at most three approver-only
policy, environment, or team-norm choices. Defects stay in Findings; if no
question exists, write `none`.
