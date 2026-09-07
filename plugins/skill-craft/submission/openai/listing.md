# OpenAI portal listing

Portal-only copy for the Skill Craft 1.3.0 submission candidate. The native
manifest remains the source for fields accepted by the ingestion schema;
Support is retained here because `interface.supportURL` is not accepted.

## Identity

- Display name: Skill Craft
- Developer name: Muhammad Bahaa
- Category: Developer Tools

## Descriptions

- Plugin description: Technical review, guided walkthroughs, and a human-attention approval gate for agent skills, slash commands, and plugins — a fixed 10-dimension safety/severity audit, a clear five-part walkthrough, and a decision layer that says how much a human must read before approving. Custom-agent review and authoring are not included.
- Short description: Review skills before release
- Long description: Review agent skills as behavior before publishing. Skill Craft audits triggers, workflow safety, context cost, testing evidence, and approval readiness through a fixed ten-dimension report. It also provides a separate five-part walkthrough in the reader's language, and an approval gate that reads the review, tests, and diff and says how much a human must read before approving: none, a few pointed lines, or a deep read. Results support a human decision; they are not a security certification.

## URLs

- Homepage: https://github.com/MuhammadBahaa/majarrah-marketplace
- Repository: https://github.com/MuhammadBahaa/majarrah-marketplace
- Website: https://majarrah-marketplace.hashnode.dev/i-built-skill-craft-because-a-skill-can-look-right-and-still-fail-at-work
- Privacy policy: https://github.com/MuhammadBahaa/majarrah-marketplace/blob/main/plugins/skill-craft/PRIVACY.md
- Terms of service: https://github.com/MuhammadBahaa/majarrah-marketplace/blob/main/plugins/skill-craft/TERMS.md
- Support: https://github.com/MuhammadBahaa/majarrah-marketplace/issues

## Starter prompts

1. Review this agent skill and tell me whether it is ready to publish.
2. Walk me through this skill in Arabic and explain what it can touch.
3. Compare these two skill versions and explain what changed.

## Limitations and release boundaries

- The target version is 1.3.0.
- Majarrah Cubiq is the authoritative source; generated majarrah-marketplace output is not edited directly.
- Preserve `.claude-plugin/plugin.json`; add `.codex-plugin/plugin.json` and keep identity fields synchronized.
- The plugin is skills-only. It has no MCP, tools, authentication, UI, telemetry, remote service, or data storage.
- The portal matrix in test-cases.json exercises the review and walkthrough skills; the approval gate's pressure scenarios are indexed in `tests/skill_approval_gate_evals.json` of the source repository.
- It does not claim security certification, full determinism, uniqueness, submission, approval, or publication.
- Verdict-to-score mapping is deterministic only after model-assigned findings and severities exist.
- The runtime ZIP excludes submission notes, tests, fixtures, the legacy manifest, repository internals, and the article cover.
- Generated ZIP files are not committed.
- Existing CI is extended; no new CI system, scanner, JSON finding engine, SARIF, or code-scanning integration is added.
- Self-review and structural checks cannot clear the independent-review gate.
- Push, tag, distribution release, portal upload, submission, and publication require separate explicit authorization.
