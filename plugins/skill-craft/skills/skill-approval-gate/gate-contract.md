# Gate Report Contract

## Contents

- Exact report skeleton
- Before-send preflight
- Vocabulary and review-Call mapping
- Worked example

Instantiate the complete exact skeleton before filling: title, Attention,
Evidence, Read, Unresolved, Decision with Recommended and Gate. Preserve
every slot name and order; replace placeholders only.

```markdown
# Approval gate: <name>
**Attention:** <NONE | FOCUSED | DEEP> — <one sentence naming the deciding evidence>
**Evidence:** review <independent <verdict> <n>/10 | self — not counted | missing> · behavior <k>/<n> required cases pass · change <new skill | revision, <n> lines> · established <none | decided capabilities>

## Read
<none-or-rows>

## Unresolved
<none-or-gaps>

## Decision
**Recommended:** <recommendation>
**Gate:** <gate-state>
```

`<none-or-rows>` is exactly `none`, or this table followed by one closing
line:

| # | Where | Why | Decide |
|---|---|---|---|
| 1 | [<file>:<line>](<cwd-relative-path>:<line>) | <evidence-backed reason> | <the one decision> |
Everything else: no read — covered by <evidence>.

`<none-or-gaps>` is exactly `none`, or one line per gap in the form
`<what is missing> → <what closes it>`.

## Before-send preflight

Before sending, silently run this internal mandatory check; never emit its
heading, checklist, or pass result. The user-facing report ends at
`**Gate:**`. Rewrite the report before sending if any check fails:

- Top lines match exactly: `# Approval gate: <name>`, then
  `**Attention:** <level> — <one sentence>`, then
  `**Evidence:** review … · behavior … · change … · established …`.
- `**Attention:**` is exactly one of `NONE`, `FOCUSED`, `DEEP`.
- `## Read` is exactly `none`, or the four-column table
  `| # | Where | Why | Decide |` with separator `|---|---|---|---|`, every
  Where cell a clickable `[<file>:<line>](<path>:<line>)` link (or
  `chat claim — no file` for a claim that exists only in chat), every
  Decide cell a decision, then the line
  `Everything else: no read — covered by <evidence>.`
- `## Unresolved` is exactly `none` or one line per gap containing the
  literal spaced ` → `.
- `## Decision` contains exactly two nonblank lines in this order:
  `**Recommended:**` then `**Gate:**`; nothing before, between, or after.
- NONE requires: Read `none`, Unresolved `none`, Gate `closed — …`, and
  Recommended `approve` or `approve — queue <F-refs>`.
- FOCUSED and DEEP require at least one Read row and always pair with
  Gate `open — closes when <what>`; only NONE closes the gate.
- A `self` or `missing` review never yields NONE, and Recommended names an
  independent review.
- Recommended never relaxes the review Call: it is at or above the weakest
  allowed value in the review-Call table below.
- The report contains no severity token of its own
  (`[blocker]`, `[major]`, `[minor]`, `[polish]`) except when citing a
  review finding by its F-id.
- No Read row says "read carefully" or "read the whole file", and none
  names unchanged, established, or evidence-covered text.
- The level is never lower than the floor of any undecided capability, and
  never lowered after pressure.

## Vocabulary and review-Call mapping

`**Recommended:**` is exactly one of:

- `approve`
- `approve — queue <F-refs>` (comma-separated, `F1, F2`)
- `approve after the reads above`
- `approve after the reads above — queue <F-refs>`
- `changes required — <what>`
- `do not approve — human first`

`**Gate:**` is exactly one of:

- `closed — reopen only on a new finding, a changed high-risk section, a behavior mismatch, or a new capability`
- `open — closes when <what>`

| Review Call | Weakest allowed Recommended | Stricter allowed |
|---|---|---|
| `approve as-is` (READY) | `approve` | `approve after the reads above`, `changes required — <what>` |
| `approve — queue the listed fixes` (READY-WITH-FIXES) | `approve — queue <F-refs>` | `approve after the reads above — queue <F-refs>`, `changes required — <what>` |
| `hold — fix the majors, then re-review` (NEEDS-WORK) | `changes required — <what>` | `do not approve — human first` |
| `do not approve — F<n> needs a human first` (BLOCKED) | `do not approve — human first` | none |
| review `self` or `missing` | `changes required — obtain an independent skill-craft-review` | none |

## Worked example

A second round after fixes, where the human already accepted the one
external write in round one:

```markdown
# Approval gate: android-release-guardian
**Attention:** NONE — independent review clean, five required behavior cases pass, no undecided capability, no open question.
**Evidence:** review independent READY 10/10 · behavior 5/5 required cases pass · change revision, 41 lines · established GitHub PR comment write (bounded, accepted round 1)

## Read
none

## Unresolved
none

## Decision
**Recommended:** approve
**Gate:** closed — reopen only on a new finding, a changed high-risk section, a behavior mismatch, or a new capability
```
