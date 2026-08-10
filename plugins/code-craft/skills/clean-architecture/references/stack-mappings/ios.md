# iOS (Swift) stack mapping

> Answers the [mapping contract](../stack-detection.md#7-what-every-mapping-must-answer).
> Defaults here fill gaps only — the project's own conventions win (precedence §4).

## 1. Layer shapes

| Concept | iOS shape |
|---|---|
| Entity / value object | `struct`/`enum` in `Domain/Models/` — Foundation only, no UIKit/SwiftUI/CoreData |
| Use case | protocol + conforming `struct`/`final class` with one `execute(…)` (or `callAsFunction`), dependencies via `init` |
| Repository contract | `protocol` in `Data/Repositories/`, beside its implementation, `async throws` (or the project's Combine idiom) returning domain types |
| Repository implementation | type in `Data/Repositories/` composing remote + local sources |
| Remote source | URLSession/Alamofire service + `Codable` DTOs in `Data/Remote/` |
| Local source | CoreData/SwiftData/GRDB/Realm behind a source type in `Data/Local/` — managed objects never escape it |
| Mappers | `init(dto:)` / `toDomain()` beside the DTOs (or the project's mapper types) |
| State holder | `@Observable` / `ObservableObject` view model (SwiftUI), presenter (UIKit), or the project's TCA reducer |

```swift
struct SaveArticleUseCase {
    let repository: SavedArticlesRepository
    func execute(id: ArticleID) async -> Result<Void, AppError> {
        await repository.save(id: id)
    }
}
// The view model calls the use case — never URLSession, the store, or the repository impl.
```

## 2. Role inventory hints (read `Package.swift` / `Podfile` / project file)

| Role | Common choices |
|---|---|
| DI | manual `init` injection / Factory / Swinject / Needle / SwiftUI `Environment` |
| HTTP | URLSession (no dependency) / Alamofire / Moya |
| Storage | CoreData / SwiftData / GRDB / Realm / UserDefaults / Keychain |
| Concurrency | async-await vs Combine vs RxSwift — follow the project |
| Navigation | NavigationStack / coordinator types / UIKit segues |
| Serialization | `Codable` (DTOs only) |
| Testing | XCTest / swift-testing; fakes via protocol conformance (little mocking-library culture) |

## 3. Banned imports per layer

`Domain/` and `UseCases/`: no `import UIKit`, `SwiftUI`, `CoreData`, `SwiftData`, `Alamofire`,
`RealmSwift`, Firebase. `Foundation` is fine. Keep domain async/await-pure; `Combine` only if
the project's domain already uses it.

`Presentation/`: no DTOs, no storage/HTTP imports; view models import use cases and domain
types, never `Data/` internals.

```bash
grep -rn "import UIKit\|import SwiftUI\|import CoreData\|import SwiftData\|import Alamofire\|import RealmSwift" Sources/**/Domain/ && echo VIOLATION
```

Use cases may import **repository and gateway protocols** from `Data/` — that is where those
interfaces live. What they must not import is anything concrete behind them: implementations,
stores, services, or DTOs. Entities import nothing from `Data/` at all.

(Adapt paths; if the project modularizes with SPM, the strongest check is making the Domain
target depend on nothing but Foundation and use-case code on nothing but Domain plus the
contract protocols — the compiler becomes the architecture test.)

## 4. Composition root

The `App` struct / `AppDelegate` / the project's assembly-container file. It builds sources →
repository impls (typed as the domain protocols) → use cases → view models, and hands them
down via init or Environment. Views and use cases never construct URLSession clients, stores,
or repositories.

## 5. Test idiom

`swift test` for SPM domain/data modules, `xcodebuild test -scheme <app>` otherwise. Domain
and use-case tests are plain XCTest with protocol-conforming fakes; view-model tests fake the
use cases; repository tests use in-memory stores / stubbed `URLProtocol`. No simulator needed
for business behavior.

## Greenfield fallbacks (no project convention found)

- Layout: `Features/<Feature>/{Presentation,Domain,Data}` groups (or SPM targets when the
  project already modularizes).
- Result/error idiom: `Result<T, AppError>` with a small `AppError: Error` enum; translate
  `URLError`/store errors in `Data/`.
- State holder: `@Observable` view model exposing a `ViewState` enum with
  `loading / content / empty / error` cases.
- Use case naming: `VerbNounUseCase` with a single `execute(…)`.
