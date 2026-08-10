# Flutter stack mapping

> Answers the [mapping contract](../stack-detection.md#7-what-every-mapping-must-answer).
> Defaults here fill gaps only — the project's own conventions win (precedence §4).

## 1. Layer shapes

| Concept | Flutter shape |
|---|---|
| Entity / value object | plain Dart class (`equatable`/`freezed` only if the project already uses them in domain) |
| Use case | class with a single `call()` method, dependencies via constructor |
| Repository contract | `abstract class`/`abstract interface class` in `data/repositories/`, beside its impl |
| Repository implementation | class in `data/repositories/` composing remote + local sources |
| Data sources | `abstract class` + impl per side in `data/datasources/` (`remote`/`local`) |
| API/DB model | `data/models/`, with `fromJson`/`toJson` and a `toDomain()` (or the project's mapper idiom) |
| State holder | whatever the project uses — Bloc/Cubit, Riverpod notifier, Provider ChangeNotifier, GetX controller |

```dart
// domain/usecases/get_saved_articles.dart
class GetSavedArticles {
  final SavedArticlesRepository repository;
  GetSavedArticles(this.repository);
  Future<Result<List<Article>>> call() => repository.getSavedArticles();
}
// presentation state holder calls the use case — never the repository impl:
// final result = await getSavedArticles();
```

## 2. Role inventory hints (read `pubspec.yaml`)

| Role | Common packages |
|---|---|
| State management | `flutter_bloc` / `riverpod`·`flutter_riverpod` / `provider` / `get` / `mobx` |
| DI | `get_it` (+`injectable`) / riverpod providers / `provider` / GetX bindings |
| HTTP | `dio` / `http` / `chopper` / `retrofit` (dart) / `graphql_flutter` |
| Storage | `drift` / `isar` / `hive` / `sqflite` / `shared_preferences` / `flutter_secure_storage` |
| Navigation | `go_router` / `auto_route` / Navigator 1.0 |
| Serialization | `json_serializable` / `freezed` / manual `fromJson` |
| Testing | `flutter_test` + `mocktail` / `mockito` / `bloc_test` |

## 3. Banned imports per layer

`domain/` (and use cases, wherever the project keeps them) must not import:
`package:flutter/…`, `dart:ui`, any state-management package, `package:dio/…` or other HTTP
clients, any storage package, `package:get_it/…`.

Use cases may import **repository and gateway contracts** from `data/repositories/` — that is
where those interfaces live. What they must not import is anything concrete behind them:
`*Impl` classes, data sources, or models. Entities import nothing from `data/` at all.

`presentation/` must not import `data/` implementations, models, or HTTP/storage packages.

```bash
grep -rn "package:flutter/\|package:dio\|package:http/\|package:hive\|package:drift\|package:sqflite\|package:shared_preferences\|package:get_it" lib/features/*/domain/ && echo VIOLATION
grep -rn "/data/" lib/features/*/presentation/ --include="*.dart" | grep import && echo VIOLATION
```

(Adapt both globs to the project's actual layout first — a glob that matches no files prints
nothing, which reads as a false pass. Prefer the project's own arch-test tooling when present.)

## 4. Composition root

Wherever the project already wires things: a `service_locator.dart` / `injection_container.dart`
(get_it), `ProviderScope` overrides (riverpod), or top-level `MultiProvider`/bindings. Register
new feature dependencies there — data sources → repository impl (bound to the domain contract)
→ use cases → state holder factory. Widgets and use cases never construct their own `Dio`,
database, or repository.

## 5. Test idiom

`flutter test`. Domain and use-case tests are pure Dart (`test()` with fakes — `mocktail` if
present). State-holder tests fake the use cases (`bloc_test` when the project uses bloc).
Repository tests fake the data sources. No emulator for any of it.

## Greenfield fallbacks (no project convention found)

- Layout: `lib/features/<feature>/{presentation,domain,data}` with
  `domain/{entities,usecases}` and `data/{models,datasources,repositories}` — the repository
  contract and its impl both sit in `data/repositories/`.
- Result/error idiom: a small sealed result in `core/` (`Success<T>` / `Failure(AppError)`);
  domain errors as an enum or sealed class. Do not add `dartz`/`fpdart` just for this.
- State holder: use the state-management package the manifest already has; if there is truly
  none, `ChangeNotifier` (framework-built-in) — never add a new package unprompted.
- UI state: one immutable state type with explicit `loading / content / empty / error`.
