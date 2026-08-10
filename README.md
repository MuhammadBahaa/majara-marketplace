# Majarrah Nexus — Marketplace

[![Latest release](https://img.shields.io/github/v/release/MuhammadBahaa/majarrah-marketplace?display_name=release&label=release&color=brightgreen)](https://github.com/MuhammadBahaa/majarrah-marketplace/releases)
[![License](https://img.shields.io/github/license/MuhammadBahaa/majarrah-marketplace)](LICENSE)
[![Stars](https://img.shields.io/github/stars/MuhammadBahaa/majarrah-marketplace?style=flat)](https://github.com/MuhammadBahaa/majarrah-marketplace/stargazers)
[![skills.sh installs](https://skills.sh/b/MuhammadBahaa/majarrah-marketplace)](https://skills.sh/MuhammadBahaa/majarrah-marketplace)

Free, open AI-agent skills from **Majarrah Nexus**. Works with Codex, Claude
Code, and every agent that supports the Agent Skills open standard — including
Cursor, GitHub Copilot, and Gemini CLI.

> This repository is **generated** from the private `MajarrahCore` monorepo.
> Do not edit here — changes are overwritten on the next release.

## Plugins

| Plugin | What it does |
|--------|--------------|
| [`skill-craft`](plugins/skill-craft) | Technical review and guided walkthroughs for agent skills, slash commands, and plugins. |
| [`code-craft`](plugins/code-craft) | Clean Architecture feature implementation in whatever stack a project already uses. |

## Install

Every route installs the same skills. Pick the one that matches your agent.

### Codex

```bash
codex plugin marketplace add MuhammadBahaa/majarrah-marketplace
codex plugin marketplace list
codex plugin list
codex plugin add skill-craft@majarrah-marketplace
codex plugin add code-craft@majarrah-marketplace
```

`codex plugin list` should now show `skill-craft@majarrah-marketplace` and
`code-craft@majarrah-marketplace` as `installed, enabled`. Start a
new Codex task to load the skills.

### Claude Code

```bash
claude plugin marketplace add MuhammadBahaa/majarrah-marketplace
# then, inside Claude Code:
/plugin install skill-craft@majarrah-marketplace
/plugin install code-craft@majarrah-marketplace
```

`/plugin` lists what is installed — `skill-craft` and `code-craft` should both
be enabled. Start a new session to load the skills.

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
project). Restart the agent afterwards.

## License

[MIT](LICENSE) © Majarrah Nexus
