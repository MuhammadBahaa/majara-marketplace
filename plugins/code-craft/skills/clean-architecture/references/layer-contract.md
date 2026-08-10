# Layer contract — the rules every feature obeys

> Stack-neutral. What each concept *looks like* in the detected stack comes from its
> [stack mapping](stack-detection.md#6-load-a-bundled-mapping-or-derive-one-live); the project's
> own conventions choose names and tools. These rules say what must be true regardless.

## Contents

1. The one rule — dependency direction · 2. Domain · 3. Application — use cases ·
4. Repository and gateway contracts · 5. Data · 6. Presentation · 7. State management ·
8. Navigation · 9. Offline and synchronization · 10. Composition root · 11. Testing matrix ·
12. When to skip layers

## The one rule — dependency direction

```
Frameworks & drivers (UI, web, devices, databases) → interface adapters → application use cases → domain
```

Source-code dependencies point **inward only**. The domain knows nothing outside itself; use
cases know the domain; adapters (presentation, data) know use cases and domain; frameworks are
wired at the edge. Anything that breaks this direction is a violation — report it, never hide it.

**One deliberate exception:** use cases name the repository and gateway **contracts**, which
live in the data layer (see *Repository and gateway contracts*). That reference is to an
abstraction stated in domain language — never to an implementation, data source, API/DB model,
or framework type, all of which stop at the data layer's edge. The domain proper still imports
nothing outside itself.

**Feature-first organization.** Each feature carries its own layers:

```
features/
  orders/
    presentation/   application/   domain/   data/
```

Folder names follow the project's existing scheme (some projects use `ui/`, `usecases/`,
`infrastructure/` — keep theirs). Extract shared code only when a second feature genuinely uses
it, not speculatively.

## Domain

Contains: entities, value objects, business invariants, domain errors, and pure domain services
for behavior that belongs to no single entity. Repository and gateway contracts live with their
implementations in the data layer — see *Repository and gateway contracts* below.

The domain must not import, in any stack:

- UI or web frameworks — widget APIs, component frameworks, server web frameworks and their
  decorators/annotations
- State-management libraries
- HTTP clients
- Database, ORM, or storage libraries — including their model/annotation types
- Analytics, notifications, device, or infrastructure APIs

Test bar: domain code runs as ordinary unit tests — no device, simulator, UI framework,
database, or network. If a domain test needs any of those, the domain is contaminated.

## Application — use cases

One focused use case per meaningful user operation: `SignIn`, `LoadProfile`, `UpdateProfile`,
`SubmitOrder`, `SyncOfflineChanges`, `EnableNotifications`.

Each use case:

- Represents exactly one application operation
- Takes simple framework-independent input; returns a framework-independent result — never
  framework state objects or vendor exceptions
- Coordinates entities, repositories, and gateways; **business rules live in domain objects,
  use cases orchestrate them**
- Declares dependencies through constructor injection
- Contains no UI, navigation, platform, HTTP, or database logic

## Repository and gateway contracts

**A repository contract lives in the data layer, beside its implementation** — the abstraction
and the thing it abstracts stay together, so everything that knows about a data source sits in
one place. Use cases depend on the contract; the data layer owns it:

```
data/
  repositories/
    OrderRepository.kt        <- contract
    OrderRepositoryImpl.kt    <- implementation
```

Contracts speak domain language and hide REST, GraphQL, SQLite, Room, Core Data, Realm,
Firebase, and cache details. They never expose HTTP responses, database rows, ORM models, or
framework types — a caller reading the interface should not be able to tell what is behind it.
One repository per aggregate or meaningful domain boundary — never one per table.

```
prefer:  orderRepository.getPendingOrders()      orderRepository.save(order)
avoid:   orderRepository.selectFromOrdersTable() orderRepository.updateRow(...)
```

Platform capabilities get the same treatment — a gateway contract beside its implementation,
exposing no platform objects: camera, location, biometrics, secure storage, push notifications,
file system, connectivity, permissions, background tasks (`AuthenticationGateway`,
`LocationGateway`, `NotificationPermissionGateway`, `ConnectivityGateway`, …).

**On the other arrangement.** Classic Clean Architecture inverts this: the contract is declared
in the inner layer that consumes it, so nothing inner ever names anything outer. That is a
sound design, and a project already built that way keeps it (convention precedence) — but it is
not this skill's default, because the placement above is what mainstream mobile guidance and
most real mobile codebases use, and keeping an interface far from its only implementation buys
little on a codebase this shape. Either way the rule that actually matters is unchanged: the
contract is stated in domain language, and API, database, and framework types stop at the data
layer's edge.

## Data

Owns the repository and gateway contracts **and** implements them. Keep remote and local
sources separate:

```
data/
  remote/   local/   repositories/   mappers/   models/
```

- The repository implementation decides where data comes from — network, cache, or local
  database. Callers never know.
- Convert explicitly at every boundary: `API model ↔ data model ↔ domain entity`. API and
  database models never reach use cases or presentation.
- Translate technical errors here, at the outer boundary:

| Technical failure | Application error |
|---|---|
| HTTP timeout / no connection | `NetworkUnavailable` |
| SQLite/storage error | `LocalStorageFailure` |
| Permission denied | `LocationPermissionDenied` (per capability) |
| Expired token / 401 | `AuthenticationRequired` |

Use cases and UI never see vendor-specific exceptions. Presentation converts application
errors into user-facing messages.

## Presentation — the delivery mechanism

On UI surfaces: screens/views plus the project's state holders (view model, presenter,
controller, BLoC, store). On services: the controllers, route handlers, resolvers, and
presenters that parse transport input, call a use case, and map its result to a response.

- State holders and controllers call **use cases, never repository implementations** — and
  never data sources.
- No business rules in delivery. If an `if` encodes policy, it belongs further in.
- On UI surfaces, use-case results become **immutable UI state** with explicit `loading /
  content / empty / error` states; rendering stays separate from state transitions. On
  services, use-case results and application errors map to transport responses and status
  codes — never vendor exceptions serialized to clients.
- No direct access to network, database, analytics, or device/infrastructure APIs.

Required flow, in both directions:

```
User action or request → state holder / controller → use case → repository contract
                       → repository implementation → local or remote data source
```

## State management (UI surfaces)

Use the project's existing approach — never introduce a competing one. Regardless of library:

- UI state is immutable; persistent domain state and temporary UI state stay separate.
- No business rules inside reducers, BLoCs, view models, or controllers.
- Prevent duplicated in-flight requests across screen recreation (rotation, tab revisit).
- Model cancellation, retry, refresh, and stale-data behavior explicitly.
- Never store navigation or UI objects inside domain entities.

## Navigation (UI surfaces)

Navigation belongs to the presentation/framework boundary. (On services, the analog is
routing configuration — it lives with the delivery layer and never leaks inward.) Use cases return **outcomes**
(`AuthenticationSucceeded`), never navigate. State holders or coordinators translate outcomes
into navigation events. Domain and application code never references routes, screens,
activities, fragments, view controllers, or navigation contexts.

## Offline and synchronization

When offline support is required, the proposal must state explicitly — never buried in screens
or HTTP clients:

source of truth · cache lifetime · read policy · write policy · optimistic-update behavior ·
retry policy · conflict resolution · how sync status is shown to the UI.

## Composition root

Concrete implementations are wired **only** in the app's composition root (per-stack location
in the mapping: application module/DI modules, app assembly, registration module, app
container). Inner layers never instantiate concrete repositories, HTTP clients, databases, or
platform services.

## Testing matrix

| Layer | Test | Doubles |
|---|---|---|
| Domain | unit tests for invariants | none needed |
| Use cases | unit tests | fake repositories and gateways |
| State holders / controllers | unit tests | fake use cases |
| Delivery routes (services) | thin integration tests (request → response mapping) | fake use cases |
| Repository implementations | integration tests (remote + local behavior) | test server / in-memory db per project idiom |
| Mappers | unit tests | none |
| Offline/sync | policy tests when relevant | fakes + controlled connectivity |
| Architecture | dependency-direction checks (greps or the project's arch-test tool) | — |

Most business behavior must be testable without an emulator, simulator, or physical device.

## When to skip layers

A feature with **no meaningful business boundary** doesn't get ceremony:

- A purely static screen needs no use case, repository, or data layer.
- A thin read-through with zero rules may use one slim use case and one contract — not empty
  pass-through classes at every layer.

Two constraints: a skipped layer is a **recorded decision in the proposal**, never a silent
shortcut; and skipping never applies to the boundaries themselves — dependency direction,
model conversion at data edges, and error translation hold even for small features.

**"The project already fills that role with something else" is not a skip — it is a structural
conflict.** Leaning on an existing seam that breaks the contract (a repository role played by a
`*UseCase` god-interface, a data source doubling as a use case) looks like avoiding ceremony,
but it decides the feature's shape on the operator's behalf. Both paths are defensible — reuse
the seam and stay consistent, or give this feature the narrow contract the layer calls for — so
ask, then record which they picked. See SKILL.md Step 2, *Structural conflicts*.
