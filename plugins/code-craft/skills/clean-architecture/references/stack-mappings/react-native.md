# React Native stack mapping

> Answers the [mapping contract](../stack-detection.md#7-what-every-mapping-must-answer).
> Defaults here fill gaps only — the project's own conventions win (precedence §4).

## 1. Layer shapes

| Concept | React Native shape |
|---|---|
| Entity / value object | TypeScript type/interface + pure functions (or class) in `domain/entities/` |
| Use case | pure async function built by a factory that closes over its dependencies, or a class — one operation each, in `domain/usecases/` (or `application/`) |
| Repository contract | TS `interface` in `data/repositories/`, beside its implementation, using domain types |
| Repository implementation | object/class in `data/repositories/` composing remote + local sources |
| Remote source | axios/fetch client + DTO types in `data/remote/` |
| Local source | AsyncStorage/MMKV/WatermelonDB/SQLite wrapper in `data/local/` |
| Mappers | `toDomain(dto)` functions in `data/mappers/` (with zod/io-ts validation when the project uses it) |
| State holder | the project's: Redux Toolkit slice + thunks, zustand store, MobX store, or plain hooks |

```ts
// domain/usecases/saveArticle.ts
export const makeSaveArticle =
  (repo: SavedArticlesRepository) =>
  async (id: ArticleId): Promise<Result<void>> =>
    repo.save(id);
// A hook/thunk calls the built use case — never axios, storage, or the repository impl.
```

**Query-cache libraries (react-query / RTK Query):** these are presentation-side caching. Keep
the boundary by having the query function call a **use case** (`useQuery({ queryFn: () =>
getSavedArticles() })`), never raw `fetch`/axios inline in components. Server-cache policy
(staleTime, retry) stays in presentation; source-of-truth and offline policy stay in the
repository.

## 2. Role inventory hints (read `package.json`)

| Role | Common packages |
|---|---|
| State management | `@reduxjs/toolkit` / `zustand` / `mobx` / `jotai` / `@tanstack/react-query` (server cache) |
| DI | manual factory wiring / React Context providers / rarely inversify |
| HTTP | `axios` / `fetch` / `@apollo/client` |
| Storage | `@react-native-async-storage/async-storage` / `react-native-mmkv` / `@nozbe/watermelondb` / `expo-sqlite` / Realm |
| Navigation | `@react-navigation/*` / `expo-router` |
| Validation | `zod` / `io-ts` / none |
| Testing | `jest` + `@testing-library/react-native`; `detox` for e2e |

## 3. Banned imports per layer

`domain/` (and use cases): no `react`, `react-native`, navigation, axios/fetch wrappers,
storage packages, or state-management imports — types and pure functions only. Use cases may
import **repository and gateway interfaces** from `data/repositories/` (that is where they
live), never anything concrete behind them: implementations, sources, clients, or DTOs.

`presentation/` (components, hooks, stores): no `data/` imports, no direct axios/storage —
only use cases and domain types.

```bash
grep -rn "from 'react\|from \"react\|from 'axios\|@react-navigation\|async-storage\|react-native-mmkv" src/features/*/domain/ && echo VIOLATION
grep -rn "/data/" src/features/*/presentation/ | grep -E "import|require" && echo VIOLATION
```

(Adapt both globs to the project's actual layout first — a glob that matches no files prints
nothing, which reads as a false pass. ESLint `import/no-restricted-paths` is the durable form
when the project already lints.)

## 4. Composition root

One `container.ts`/`di.ts` (or the app entry) builds the graph at startup: clients → data
sources → repository impls (typed as the domain interfaces) → use cases — exposed to the tree
via a Context provider or imported factory results. Components and use cases never build
clients or repositories themselves.

## 5. Test idiom

`jest` in node env for domain, use cases (fake repositories as plain objects), and mappers;
`@testing-library/react-native` for components with use cases faked via the provider. No
emulator for business behavior.

## Greenfield fallbacks (no project convention found)

- Layout: `src/features/<feature>/{presentation,domain,data}`.
- Result/error idiom: a discriminated union `{ ok: true; value } | { ok: false; error:
  AppError }` in `core/`; translate axios/storage errors in `data/`.
- State holder: hooks calling use cases, with whatever store the manifest already has; add
  nothing new unprompted.
- UI state: explicit `loading / content / empty / error` in one immutable state object.
