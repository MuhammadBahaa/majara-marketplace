# Stack detection and project profile — detect, inventory, adapt

> The architecture method is stack-agnostic; everything stack-specific lives in a **stack
> mapping**. This file is the contract: how the stack is detected, how the project's packages
> and conventions are inventoried into an auditable **Project Profile**, which conventions win,
> and what any mapping — bundled or derived live — must answer.

## Contents

1. Detect the stack · 2. Inventory packages by role · 3. Read the existing conventions ·
4. Precedence — who wins · 5. The Project Profile block · 6. Load a bundled mapping or derive
one live · 7. What every mapping must answer

## 1. Detect the stack

Check signals **in this order** — wrappers and shells embed the stacks below them, so their
signals outrank the embedded ones:

| Order | Signal | Stack |
|---|---|---|
| 1 | `pubspec.yaml` | flutter |
| 2 | `package.json` with a `react-native` dependency | react-native |
| 3 | `package.json` with electron / tauri | desktop shell *(derive live)* |
| 4 | `build.gradle*` with a Kotlin Multiplatform plugin | kmp *(derive live)* |
| 5 | `build.gradle` / `build.gradle.kts` / `AndroidManifest.xml` | android |
| 6 | `*.xcodeproj` / `*.xcworkspace` / `Package.swift` (app targets) | ios |
| 7 | `package.json` with next / nuxt / remix / sveltekit | web meta-framework *(derive live — has a client and a server side; ask which side the feature is)* |
| 8 | `package.json` with react / vue / angular / svelte, no server framework | web frontend *(derive live)* |
| 9 | `package.json` with nest / express / fastify / koa / hono, no frontend framework | node-backend |
| 10 | `pom.xml` / `build.gradle*` without Android plugins | jvm-backend *(derive live)* |
| 11 | `pyproject.toml` / `requirements.txt` with django / fastapi / flask | python-backend *(derive live)* |
| 12 | `go.mod` · `Gemfile` + rails · `composer.json` + laravel · `*.csproj` | go / ruby / php / .NET backend *(derive live)* |

- **One clear winner** → record `stack: <name>` in the Project Profile.
- **Multiple candidates or none** (a monorepo with several apps, an SSR app with API routes)
  → ask the operator which app or side the feature belongs to — **never guess**.

## 2. Inventory packages by role

Read the manifest (`pubspec.yaml`, Gradle dependency blocks, `Package.swift` + `Podfile`,
`package.json`, `pyproject.toml` / `requirements.txt`, `go.mod`, `pom.xml`, `composer.json`,
`Gemfile`) and fill every row. A role can be empty; UI-only roles are n/a on services.

| Role | What fills it |
|---|---|
| Delivery / web framework *(services)* | the framework handling transport (nest, express, spring, fastapi, …) |
| State management *(UI surfaces)* | the library presentation state holders use |
| Dependency injection | container / codegen / manual factories |
| HTTP / network | client library for outbound calls |
| Local storage / database | db, ORM, key-value, secure storage |
| Navigation *(UI surfaces)* | router / navigation library |
| Serialization / validation | JSON codegen, runtime parsing, schema validation |
| Testing | test framework, mocking, fixtures |

Record **evidence** for each filled role (manifest line). An unfilled role gets the stack
mapping's fallback default — recorded as `default (no project convention)`.

**A filled role is binding.** The feature relies on the package the project already has —
its DI container does the wiring, its HTTP client backs the remote source, its storage
package backs the local source, its state-management library shapes the state holder.
Proposing an alternative for a filled role is a violation, not a preference.

## 3. Read the existing conventions

**Study how this project already builds features before planning anything**, in this order —
an earlier source settles what a later one would have to guess:

1. **The project's own guidance** — project-local skills, agent instructions (`CLAUDE.md`,
   `AGENTS.md`), and architecture or contributing docs that describe the project's workflow.
   When the project documents how its features are structured, that documentation is the
   authority.
2. **The project's history** — the commits that added the last few features (`git log`, the
   diff of one recent feature): they show which layers, folders, and packages a finished
   feature actually touches.
3. **Your own search** — when neither exists, derive the conventions directly from the code:
   look at up to three existing features (or the whole `lib`/`src` tree when there are none).

Record what the study found, each with one example path (or doc/commit reference):

- Folder scheme and layer names actually used (`presentation` vs `ui`, `domain`, `data`, …)
- Naming suffixes: use cases (`*UseCase` / `*Interactor` / verb classes), contracts
  (`*Repository` / `*Gateway`), state holders (`*ViewModel` / `*Bloc` / `*Controller` /
  `*Store`), UI state types
- Error/result idiom: sealed result type, `Either`, thrown domain errors, discriminated unions
- Mapper idiom: extension functions, `toDomain()` methods, standalone mapper classes
- Where DI registration happens (the composition root the project already has)

No existing structure at all → record `conventions: greenfield — mapping defaults apply`.

## 4. Precedence — who wins

1. **The project's existing convention wins over this skill's defaults** — naming, state
   management, DI, error type, folder names. New code must read like the project wrote it.
2. **The layer contract's boundaries win over convention.** If existing code violates the
   dependency direction (screens calling HTTP, API models in widgets), that is a **divergence**:
   new code does not copy it, the report names it, and existing code is not rewritten beyond
   the feature's scope.
3. **When the convention *is* the divergence, ask — don't resolve it silently.** Rule 2 covers
   code that breaks the contract *around* the feature. This covers the case where the project's
   own shape for a layer breaks it and the feature has to sit on that shape (the trigger cases
   and question template live in SKILL.md Step 2, *Structural conflicts*). Put the choice to
   the operator before building and record their answer on the profile's `structural conflicts`
   line; with no answer, build to the layer contract and record the conflict as unresolved.
   Scope is a good reason not to rewrite the rest of the codebase; it is not a reason not to ask.
4. **Never introduce a competing package** for a role the project already fills. A missing
   role may be filled with the mapping's fallback — smallest viable choice, recorded in the
   profile.
5. **Two conflicting conventions** for the same thing (half the features use `*Interactor`,
   half `*UseCase`) → ask the operator which one this feature follows — never guess.

## 5. The Project Profile block

Paste this, filled, at the top of the proposal (Step 2 of the workflow) so the derived
mapping is auditable before any code exists:

```
## Project Profile
stack: <detected>            evidence: <file>
existing architecture: <feature-first clean layers / partial / none>   example: <path>
conventions learned from: <project guidance / git history / code search>   reference: <doc, commit, or path>
packages by role:
  state management: <pkg or default>        (<manifest line or "fallback">)
  dependency injection: <…>                 (<…>)
  delivery/web framework (services): <…> · http: <…> · storage: <…>
  navigation (UI): <…> · serialization/validation: <…> · testing: <…>
conventions:
  use case naming: <…>   contract naming: <…>   state holder: <…>
  error/result idiom: <…>   mapper idiom: <…>   composition root: <path>
gaps filled by mapping defaults: <list or none>
divergences observed (not copied, not rewritten): <list or none>
structural conflicts raised → operator's decision: <conflict → "project style" | "correct shape", or none>
```

## 6. Load a bundled mapping or derive one live

- A bundled mapping exists at [`stack-mappings/`](stack-mappings/)`<stack>.md` (flutter,
  android, ios, react-native) → follow it, with the profile's conventions overriding its
  defaults per §4.
- **No bundled mapping** (kmp, MAUI, Ionic, anything else) → derive one live from the
  project's own conventions, answer the contract below, and include the derived mapping in
  the proposal so it is reviewable.

## 7. What every mapping must answer

1. **Layer shapes** — what an entity, use case, repository contract, repository
   implementation, data source, mapper, and state holder concretely look like in this stack.
2. **Role inventory hints** — the common packages per role and how to spot them in the
   manifest.
3. **Banned imports per layer** — concrete import prefixes that must not appear in domain and
   application code, plus runnable check commands.
4. **Composition root** — where wiring lives in this stack.
5. **Test idiom** — frameworks, fake/mocking style, and the commands that run unit and
   integration tests without a device.
