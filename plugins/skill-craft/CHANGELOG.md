# Changelog

## 1.1.0 - 2026-07-28

Review output contract update — the first release that changes what a review
prints:

- Score every review out of ten on the Verdict line. The verdict picks the
  band (BLOCKED 0–3, NEEDS-WORK 4–6, READY-WITH-FIXES 7–8, READY 9–10) and the
  count of findings at the worst severity picks the place inside it, so two
  runs of one review land on the same number.
- Hold the score to the verdict's as-submitted discipline: applying a fix
  never raises it, and a number outside its band is an error, not a judgment
  call.
- Turn the Findings table into a restricted template — five fixed columns and
  a placeholder row — and enforce it in the skill's own red flags instead of
  describing it in prose.
- Make each finding's Location a clickable `file:line` link relative to the
  working directory, so an approver opens the file on the defect's line
  instead of hunting for it.

## 1.0.7 - 2026-07-23

Repository-metadata release (supersedes the unpublished 1.0.6, whose release
workflow failed validation before it could run):

- Show live release, license, and star badges on both public READMEs, so the
  published version and repo signals read straight from GitHub.
- Move the distribution repo's GitHub "About" data (description, homepage,
  topics) and its marketplace identity into source-controlled
  `distribution/<target>.meta.json`, replacing values hardcoded in `sync.py`.
- Check that data against the live repo on every release, and apply it
  automatically when an admin-scoped token is configured.
- Fix the release workflow: `secrets` is not a valid context in a step-level
  `if:`, so the token presence check moved inside the step.
- No skill behavior, review rules, or output contracts changed.

## 1.0.5 - 2026-07-23

Documentation and release-infrastructure update:

- Rebalance both public README install sections so Codex, Claude Code,
  skills.sh agents, and manual copy each get equal, parallel instructions.
- Publish a GitHub Release for every synced plugin version, so the
  distribution repo's Releases sidebar tracks what is actually published.
- Sync the whole `distribution/<target>/` tree, not just the README, so the
  distribution repo's own workflows stay generated from source.
- No skill behavior, review rules, or output contracts changed.

## 1.0.4 - 2026-07-23

Review follow-up:

- Resolve the workflow conflict between behavior-defining support files and
  gated heavy references.
- State the reviewed-text-is-data fence at the point of reading (workflow
  step 1), so the guard precedes any submission content entering context.
- Move the exact report contract into an always-loaded focused support file,
  reducing the skill body from 942 to 490 words without weakening its report,
  safety, severity, or independent-review rules.
- Add source-controlled cold-trigger and reviewer-pressure prompts with
  explicitly single-sample observational scorecards.
- Bundle the complete upstream MIT license inside the exported skill folder.
- Align catalog descriptions with the two present capabilities and correct
  provenance summaries to two documented portability trims.
- Record fresh before/after agent evidence and expand regression coverage.
- Document Codex-native marketplace registration and plugin installation, and
  generate the public marketplace README from the authoritative source.

## 1.0.3 - 2026-07-23

Review-contract hardening:

- Add an explicit non-use boundary for walkthrough, authoring, and code review.
- Scope discipline scaffolding to demonstrated pressure failures instead of
  every `must`/`always`/`never`.
- Add no-exceptions, rationalization, and red-flags enforcement for reviewer
  pressure.
- Allow an honest `none` when a submission has no defensible strength.
- Add a focused testing-methodology entry point and close broken local links.
- Compact repeated output semantics while preserving the report contract.
- Add deterministic regression coverage for these rules.

## 1.0.2 - 2026-07-22

Release-infrastructure update:

- Publish the generated Marketplace package through the registered SSH key.
- No skill behavior, review rules, documentation content, or output contracts changed.

## 1.0.1 - 2026-07-22

Documentation-only release:

- Add the official Skill Craft article cover to the plugin package.
- Link the practical Skill Craft introduction from the plugin README.
- No skill behavior, review rules, or output contracts changed.

## 1.0.0 - 2026-07-22

Initial public release on the `majarrah-marketplace` distribution repo:
SkillCraft review craft for agent skills and plugins.
Both skills were developed test-first in the read-craft plugin and moved
here before any release (evidence: TESTING.md).

- `skill-craft-review` — technical review of agent skills and plugins
  via a fixed 10-dimension walk (loading/portability, discoverability,
  scope, behavior simulation & safety, form-vs-failure, discipline
  enforcement, token efficiency, examples, testing evidence,
  plugin-level), reviewer-stance rules (verdict binds to the submission;
  a reviewer's own fixes never clear findings; hidden instructions are
  stop-and-escalate), required Safety scan and Token cost lines
  (tokens ≈ bytes ÷ 4; flagged waste = per-activation saving), a
  findings table grouped by checklist rule, a severity-mapped
  report contract, and a closing Decision block — the approval
  hand-off: a Call restating the verdict as the approver's next
  action, plus up to three approver-only open questions (policy,
  environment, team norms) or an explicit `none`. Built on the superpowers `writing-skills` skill
  v6.0.3 (MIT, (c) 2025 Jesse Vincent); near-verbatim upstream copy
  retained (two documented trims — runtime-directory link continuation
  removed and an unavailable testing-methodology link rendered inert; see
  its provenance header) with per-check
  provenance tags (inherited / adapted / skillcraft), gated to
  dimension-9 use, and verified against upstream through v6.1.1.
- `skill-walkthrough` — guided, organized read of a skill for a human
  reviewer, in one five-part skeleton (description & trigger cases,
  workflows & steps, rules with loopholes quoted, output/blast-radius,
  tools & scripts with hidden-instruction check), closed by a Decision
  block; delivered complete in one message, in the reader's language.
