# Changelog

## 1.2.1 - 2026-08-24

Submission-candidate corrections:

- Put the missing-target clarification gate directly in the primary review
  workflow: ask one concise question and wait when the artifact or request is
  missing or unclear.
- Make an unnamed walkthrough-language request pause for clarification instead
  of asking and then continuing in English in the same message.
- Compact both skill bodies below 500 words without removing the report,
  untrusted-data, comparison, or human-approval contracts.
- Add an early contents section to the long report contract.
- Contain target-supplied references to resolved regular files inside the
  target or plugin root. Absolute paths, parent traversal, and symlink escapes
  now require a concise authorization question and wait before any read.
- Remove the article-cover embed from the runtime README because the minimal
  ZIP intentionally excludes that asset, and link its excluded `TESTING.md`
  evidence directly to the public repository. An archive test now rejects
  broken local Markdown links and backticked Markdown paths.
- Replace squash-fragile changelog commit references with reproducible evidence
  paths. Fresh 1.2.1 outputs live under
  `tests/evidence/skill-craft/1.2.1/` and are indexed by
  `tests/skill_craft_submission_evals.json`; this remains observational evidence,
  not certification.
- No portal upload, submission, approval, publication, push, or tag is included.

## 1.2.0 - 2026-08-03

OpenAI directory submission-readiness package:

- Add the Codex-native manifest while preserving the compatibility manifest,
  stable package identity, author, license, and synchronized listing copy.
- Harden the walkthrough with an untrusted-data fence before the target read.
- Add the submission kit and its reproducible portal matrix of five positive
  and three negative cases.
- Add square listing and composer assets plus the allowlisted ZIP builder and
  archive inspection checks.
- Extend the existing validation and release CI gates to run the full tests and
  inspect the OpenAI package before distribution sync.
- Retain fresh single-sample observational behavior evidence: initial 6 PASS /
  2 FAIL, followed by 34 preserved failed outputs. The four affected review
  cases P1/P2/P3/N3 pass semantic and structural checks; the combined evidence
  index is 8 PASS / 0 FAIL with the other four observations retained. Full
  outputs live under `tests/evidence/skill-craft/1.2.0/` and are indexed by
  `tests/skill_craft_submission_evals.json`; this is not certification.
- No MCP server, scanner, SARIF output, external portal submission, approval,
  or publication is included.

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
