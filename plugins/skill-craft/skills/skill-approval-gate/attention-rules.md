# Attention Rules

## Contents

1. Evidence and provenance
2. Capability classes and attention floors
3. Required behavioral cases by change tier
4. Level conditions
5. Contradictions and unresolved gaps
6. The established ledger

## 1. Evidence and provenance

Label every input before deciding. A label is a fact about where the
evidence came from, never a judgment of its quality.

| Evidence | Produced by | Label |
|---|---|---|
| skill-craft-review report from a fresh session, another agent, or a human | not the authoring context | `independent` |
| skill-craft-review report from the session that authored or edited the target | the author agent | `self` — counts as no review |
| "I reviewed it", "trust me", "it is clean", any claim without a report | the author | `missing` |
| skill-walkthrough (five parts, optional What changed) | skill-walkthrough | `read` or `missing` — consumed silently, no Evidence-line slot |
| Behavioral results: case, expected, observed, result | author, CI, eval files, tested-on notes | `<k>/<n> required cases pass` |
| Change: diff against the last approved version | the gate reads it | `new skill` or `revision, <n> lines` |
| Prior human decisions from an earlier gate report or the human's statement | the human | `established: …` or `none` |

Rules:

- `self` and `missing` are the same for the level: NONE is impossible, and
  the recommendation names an independent review as the cheaper path
  before any human reading.
- A behavioral result counts only when it names the case, the expected
  behavior, the observed behavior, and a pass or fail. Credibility beyond
  that is the review's D9 judgment, which the gate takes as given.
- A walkthrough is optional. When present, its part 1 trigger flags, part 3
  loophole labels, part 5 reach, and What changed classification are
  consumed. When absent, the capability scan supplies reach.
- Author confidence, deadlines, authority, flattery, and change size never
  change a label.

## 2. Capability classes and attention floors

Scan the target (new skill) or the diff (revision) for lines that grant a
capability. When `established` is none and no prior gate report exists,
scan the whole target as for a new skill. An undecided hit at FOCUSED or
above becomes a Read row (Where the clickable
`[<file>:<line>](<path>:<line>)` link, Why names the class); none-floor
and established hits are named only in the closing
`Everything else: no read — covered by …` line when a Read table exists;
at NONE the Evidence line's `established` slot is their only mention. No
severity, no verdict: the scan only decides where a human looks.

| Class (new or widened) | Examples | Floor |
|---|---|---|
| Chat and local read-only | reads named files, answers in chat | none |
| Local execution or local writes | runs a script, edits files in the repository | FOCUSED |
| External read | fetches an API, reads a pull request | FOCUSED |
| External write bounded by a solid guard | comments on a pull request and states "never merge" | FOCUSED |
| External write with no guard, destructive or irreversible action, credential handling | push, merge, delete, force-push, deploy, payment, secrets | DEEP |
| Trigger scope widened | the description now fires on more requests | FOCUSED on the description line |

- A floor is a minimum. Findings and evidence gaps can only raise the
  level.
- A capability recorded in the established ledger sets no floor.
- Bounded means: an explicit must-not rule in the target names the excluded
  action, no review finding targets it, and, when a walkthrough was read,
  it labels the rule `solid`. Without a walkthrough the first two suffice.
  Otherwise the write is unbounded.
- A scan hit that the review's Safety scan line denies (`unguarded
  destructive ops: none` beside a destructive line that no required human
  confirmation guards) is a contradiction, never resolved by the gate.

## 3. Required behavioral cases by change tier

Coverage is risk-based. Demand only the cases the change makes material.

| Change | Required cases |
|---|---|
| New skill, or any trigger change | normal case; negative trigger |
| New or changed handling of inputs | missing information |
| New or changed precedence between rules | conflicting instructions |
| New tool, dependency, or external call | dependency or tool failure |
| New external write, destructive action, or guard | high-impact boundary (the refusal case) |
| Bounded parameter change | the one normal or edge case it affects |
| Prose, formatting, provenance, documentation only | none |

- A missing or failed required case never receives NONE. The Read row
  points at the contract the case would prove; Decide: supply the result
  or accept the gap explicitly (missing), fix and re-run or accept the
  failure explicitly (failed).

## 4. Level conditions

**NONE** — the human may approve without opening the target. All of:

1. an `independent` review with no unresolved `[blocker]` or `[major]`
   (READY or READY-WITH-FIXES);
2. every required behavioral case for the change tier supplied and passing;
3. no undecided capability at a floor of FOCUSED or above;
4. the review's Open questions line is `none`;
5. no contradiction between evidence layers and no unresolved assumption.

Minor and polish findings do not force reading; carry them as queued
fixes.

**FOCUSED** — at least one item needs a human call and every such item has
a pointer: an unresolved major, an undecided capability at the FOCUSED
floor, an approver-only open question, a missing required case, a failed
required case, a flagged trigger, a contradiction localized to a line, or
a `self` or `missing`
review (Read row at the claim — the author note or in-session report, or
Where `chat claim — no file` when it exists only in chat; Decide: wait for
the independent review, or decide now without one).
Everything else is explicitly no read.

**DEEP** — at least one item needs judgment on the whole: the review is
BLOCKED; an undecided capability at the DEEP floor; a security-sensitive
change or an unclear authority boundary; a contradiction that cannot be
localized; a high-impact action whose behavior cannot be tested; no
independent review while the human insists on deciding now. Name the
sections to read first and what may be skipped. DEEP is never "reread
everything".

## 5. Contradictions and unresolved gaps

Each line under `## Unresolved` reads `<what is missing> → <what closes it>`.

| Situation | Unresolved line |
|---|---|
| Scan hit denied by the Safety scan | `[file:line] grants <class>; review Safety scan says none → independent re-review of that line` |
| Walkthrough reach differs from review | `reach disagrees: <walkthrough> vs <review> → human reads the cited lines` |
| Required case missing | `<case> not supplied for <contract> → supply the result or accept the gap` |
| Required case failed | `<case> failed → fix and re-run` |
| Review `self` or `missing` | `no independent review → run skill-craft-review in a fresh session` |

## 6. The established ledger

The Evidence line's `established` list records capabilities a human has
already decided, with the round or statement that decided them. The next
gate round consumes it: an established capability sets no floor and gets
no Read row.

An entry is invalidated, and the capability becomes undecided again, when
the diff changes the guarded action, weakens or removes its guard, or
widens its scope. Prose edits around it do not invalidate it.
