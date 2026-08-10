# Code Craft

[![Latest release](https://img.shields.io/github/v/release/MuhammadBahaa/majarrah-marketplace?display_name=release&label=release&color=brightgreen)](https://github.com/MuhammadBahaa/majarrah-marketplace/releases)
[![License](https://img.shields.io/github/license/MuhammadBahaa/majarrah-marketplace)](https://github.com/MuhammadBahaa/majarrah-marketplace/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/MuhammadBahaa/majarrah-marketplace?style=flat)](https://github.com/MuhammadBahaa/majarrah-marketplace/stargazers)
[![skills.sh installs](https://skills.sh/b/MuhammadBahaa/majarrah-marketplace)](https://skills.sh/MuhammadBahaa/majarrah-marketplace)

Engineering-craft skills for coding agents, by **Majarrah Nexus**.

| Skill | What it does |
|---|---|
| `clean-architecture` | Implements, extends, or refactors a feature with Clean Architecture in whatever stack the project already uses |

## What `clean-architecture` does

It enforces one dependency direction —
`frameworks & drivers → adapters → use cases → domain` — and nothing else. It
imposes **boundaries, never tools**: packages, naming, folder shape, state
management, and error idiom are read out of the project, not chosen by the
skill.

The run has four steps:

1. **Detect and profile.** Work out the stack from repo signals, inventory the
   packages already in use by role (DI, HTTP, storage, state, navigation,
   serialization, testing), and study how the project builds features today —
   its own guidance first, then the git history of past features, then the
   code. A role the project has already filled is binding; the skill's defaults
   only apply where the project left one empty.
2. **Propose before code.** Entities, use cases, contracts, data sources,
   mappers, delivery state, wiring, offline policy — plus the layers it plans
   to skip and why. Anything ambiguous stops for your answer.
3. **Build inside-out**, gating each layer before moving outward.
4. **Verify and report honestly**: the project's own tests and
   dependency-direction checks, and every violation found — new or
   pre-existing — reported rather than quietly fixed or hidden.

Bundled stack mappings ship for **Flutter, Android, iOS, React Native, and Node
backends**. Any other stack — web frontend, another backend language, desktop —
is derived live from the project's own conventions against a documented mapping
contract, so there is no per-project setup either way.

Two behaviors are worth knowing before you install it:

- **Existing violations are reported, never copied and never silently
  rewritten.** If the screens around your feature call the API inline, the
  skill will not match that and will not go clean them up.
- **Structural conflicts are your call, not the agent's.** When the project's
  own shape contradicts the layer contract — a repository that is really a use
  case, a missing layer a neighbour absorbed — the skill stops and asks, with
  the cost of each path stated. "Follow the project" is a legitimate answer;
  the point is that it is a decision on the record.

## Limits

It is a discipline for writing code, not a verifier of code you already have:
it will not audit a codebase, and its judgments about your conventions are
model judgments. It adds no packages the project does not already have. It
needs no MCP server, network access, or credentials.

## Install

Every route installs the same skill. Pick the one that matches your agent.

### Codex

```bash
codex plugin marketplace add MuhammadBahaa/majarrah-marketplace
codex plugin marketplace list
codex plugin list
codex plugin add code-craft@majarrah-marketplace
```

`codex plugin list` should now show `code-craft@majarrah-marketplace` as
`installed, enabled`. Start a new Codex task to load `clean-architecture`.

### Claude Code

```bash
claude plugin marketplace add MuhammadBahaa/majarrah-marketplace
# then, inside Claude Code:
/plugin install code-craft@majarrah-marketplace
```

`/plugin` lists what is installed — `code-craft` should be enabled. Start a new
session to load the skill.

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
cp -r majarrah-marketplace/plugins/code-craft/skills/* ~/.agents/skills/
```

Use `~/.agents/skills/` (user-wide) or `<project>/.agents/skills/` (per
project). Cursor and Copilot also read `~/.claude/skills`, so a Claude Code
install covers them too. Restart the agent afterwards.

## License

[MIT](https://github.com/MuhammadBahaa/majarrah-marketplace/blob/main/LICENSE)
© Majarrah Nexus. No third-party code is vendored into this plugin.
