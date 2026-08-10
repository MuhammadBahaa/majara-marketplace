# Changelog

Public release history for Code Craft. Versions before 0.13.0 were private and
are not listed here; the version number is shared with the private plugin, so
the first public entry starts at 0.13.0 rather than 1.0.0.

## 0.13.0 - 2026-08-10
- First public release. Ships one skill, `clean-architecture`: Clean
  Architecture feature implementation for any stack — mobile (Flutter, Android,
  iOS, React Native), web frontend, backend service, or desktop.
- Stack, packages, and conventions are detected from the project and always win
  over the skill's defaults, so there is no per-project setup. Bundled mappings
  ship for Flutter, Android, iOS, React Native, and Node backends; every other
  stack is derived live against a documented mapping contract.
- Four-step workflow: detect and profile the project, propose the design before
  writing code, build inside-out with a gate at each layer, then verify against
  the project's own tests and dependency-direction checks.
- Published under MIT, the same terms as the rest of this marketplace.
- Installs on Codex (`codex plugin add code-craft@majarrah-marketplace`),
  Claude Code, and any agent reading the Agent Skills directory via
  `npx skills add` or a manual copy.
- Pre-existing dependency violations are reported, never copied and never
  silently rewritten. Where the project's own shape contradicts the layer
  contract, the skill stops and asks rather than deciding alone.
