# Skill Craft 1.3.0 submission-candidate notes

- Adds `skill-approval-gate`, a third skill that reads the independent
  review, the behavior evidence, the diff, an optional walkthrough, and the
  human's prior decisions, then says how much a human must read before
  approving: `NONE`, `FOCUSED` with exact `file:line` pointers and the
  decision each needs, or `DEEP` with the sections to read first.
- Treats a review from the authoring session as `self` and a bare claim as
  `missing`; neither can reach `NONE`, and the recommendation names an
  independent review as the cheaper path.
- Sets attention floors from undecided capability changes (local execution
  or writes, external reads, and guarded external writes at least `FOCUSED`;
  unguarded, destructive, irreversible, or credential handling `DEEP`) and
  carries capabilities the human already accepted as `established`.
- Requires behavior evidence by change tier instead of blanket ceremony; a
  missing required case never receives `NONE`.
- Runs a pointer-only capability scan and reports any disagreement with the
  review's Safety scan as a contradiction, never as a verdict; never relaxes
  the review's Call.
- Keeps the gate read-only like its siblings: file reading and chat, an
  untrusted-data fence, root containment, no execution, no endpoint contact.
- Leaves `skill-craft-review` and `skill-walkthrough` byte-identical to
  1.2.1; their retained evidence carries forward under a recorded-hash test.
- Retains the native skills-only OpenAI manifest, compatibility manifest,
  public policy documents, portal matrix, and manual review boundaries from
  1.2.1. The portal matrix exercises the review and walkthrough skills; the
  gate's scenarios are indexed in the source repository's
  `tests/skill_approval_gate_evals.json`.
- Prepares portal copy and local verification without uploading, submitting,
  approving, publishing, pushing, or tagging the candidate.

Review and gate results remain advisory. Human approval and independent
review remain required where applicable.
