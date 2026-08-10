# Skill Craft

[![Skill Craft — review what agents will actually do](assets/skill-craft-cover.png)](https://majarrah-marketplace.hashnode.dev/i-built-skill-craft-because-a-skill-can-look-right-and-still-fail-at-work)

[Read the article: **I Built Skill Craft — Because a Skill Can Look Right and Still Fail at Work**](https://majarrah-marketplace.hashnode.dev/i-built-skill-craft-because-a-skill-can-look-right-and-still-fail-at-work)

[![Latest release](https://img.shields.io/github/v/release/MuhammadBahaa/majarrah-marketplace?display_name=release&label=release&color=brightgreen)](https://github.com/MuhammadBahaa/majarrah-marketplace/releases)
[![License](https://img.shields.io/github/license/MuhammadBahaa/majarrah-marketplace)](https://github.com/MuhammadBahaa/majarrah-marketplace/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/MuhammadBahaa/majarrah-marketplace?style=flat)](https://github.com/MuhammadBahaa/majarrah-marketplace/stargazers)
[![skills.sh installs](https://skills.sh/b/MuhammadBahaa/majarrah-marketplace)](https://skills.sh/MuhammadBahaa/majarrah-marketplace)

Skill Craft 1.2.0 is a human-in-the-loop release gate for technical reviews
and guided walkthroughs of agent skills, slash commands, and plugins by
**Majarrah Nexus**. It helps an approver inspect behavior before release;
custom-agent review and authoring are not included.

| Skill | What it does |
|---|---|
| `skill-craft-review` | Technical review of a skill/plugin: 10-dimension walk, safety scan, severity-mapped verdict, reviewer-stance rules, Decision close for the approver |
| `skill-walkthrough` | Guided, organized read of a skill: five-part plain-language walkthrough in clear ordered parts, your language; hands the approve call to skill-craft-review |

Both skills are built on the superpowers `writing-skills` skill v6.0.3
(MIT, (c) 2025 Jesse Vincent; vendored copy verified against upstream
through v6.1.1 — near-verbatim, two documented trims). Inherited versus
customized parts are
documented in each SKILL.md's Provenance section, per-check tags in
`skills/skill-craft-review/review-checklist.md`, and the near-verbatim
upstream copy in `skills/skill-craft-review/writing-skills-upstream.md`.
The two documented trims and complete upstream MIT license are retained in
[`THIRD_PARTY_NOTICES.md`](skills/skill-craft-review/THIRD_PARTY_NOTICES.md).
Test evidence:
`TESTING.md`.

## Limits

Skill Craft is a human-in-the-loop release gate.
Findings and severities are model judgments; only the score mapping after
severity is assigned is deterministic.
It is not a security certification or a replacement for static scanning.

It reviews and explains existing skill packages. It does not provide
authoring, an MCP server, network access, authentication, or storage. See the
[privacy policy](PRIVACY.md), [terms of service](TERMS.md), and
[support policy](SUPPORT.md).

## Install

Every route installs the same two skills. Pick the one that matches your agent.

### Codex

```bash
codex plugin marketplace add MuhammadBahaa/majarrah-marketplace
codex plugin marketplace list
codex plugin list
codex plugin add skill-craft@majarrah-marketplace
```

`codex plugin list` should now show `skill-craft@majarrah-marketplace` as
`installed, enabled`. Start a new Codex task to load `skill-craft-review`
and `skill-walkthrough`.

### Claude Code

```bash
claude plugin marketplace add MuhammadBahaa/majarrah-marketplace
# then, inside Claude Code:
/plugin install skill-craft@majarrah-marketplace
```

`/plugin` lists what is installed — `skill-craft` should be enabled. Start a
new session to load both skills.

### Cursor, GitHub Copilot, Gemini CLI, and others

```bash
npx skills add MuhammadBahaa/majarrah-marketplace
```

[skills.sh](https://skills.sh/MuhammadBahaa/majarrah-marketplace) installs into
the shared Agent Skills directory these agents read. Gemini CLI alternative:
`gemini skills install <skill-folder-or-git-url>`. Reload skills or restart the
agent afterwards.

### Manual copy

```bash
git clone https://github.com/MuhammadBahaa/majarrah-marketplace
mkdir -p ~/.agents/skills
cp -r majarrah-marketplace/plugins/skill-craft/skills/* ~/.agents/skills/
```

Use `~/.agents/skills/` (user-wide) or `<project>/.agents/skills/` (per
project). Cursor and Copilot also read `~/.claude/skills`, so a Claude Code
install covers them too. Restart the agent afterwards.

## License

SkillCraft-original material is MIT. The vendored superpowers
`writing-skills` copy is covered by its complete retained
[MIT notice](skills/skill-craft-review/THIRD_PARTY_NOTICES.md).
