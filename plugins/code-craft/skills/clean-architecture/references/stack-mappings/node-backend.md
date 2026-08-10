# Node backend stack mapping

> Answers the [mapping contract](../stack-detection.md#7-what-every-mapping-must-answer).
> Defaults here fill gaps only — the project's own conventions win (precedence §4).

## 1. Layer shapes

| Concept | Node backend shape |
|---|---|
| Entity / value object | plain TS type/interface + pure functions (or class) in `domain/entities/` — no framework decorators |
| Use case | class or factory-built async function, one operation each, dependencies injected via constructor/closure |
| Repository contract | TS `interface` in `data/repositories/`, beside its implementation, using domain types |
| Repository implementation | class/object in `data/repositories/` composing db + external sources |
| Database source | pg/knex/Prisma/TypeORM/Drizzle access in `data/db/` — rows and ORM entities never leave `data/` |
| External services | HTTP clients for other APIs in `data/remote/` (or the project's `infrastructure/`) |
| Mappers | `toDomain(row)` / `toRow(entity)` functions beside the models |
| Delivery | Nest controllers / Express-Fastify routers in `presentation/` (or `routes/`, `controllers/`): parse + validate input, call a use case, map result and application errors to status codes |

```ts
// domain/usecases/cancelOrder.ts
export class CancelOrderUseCase {
  constructor(private readonly orders: OrderRepository) {}
  async execute(id: OrderId): Promise<Result<void>> {
    /* pending-only rule lives in the Order entity; this orchestrates */
  }
}
// The route handler calls the use case — never the pool, the ORM, or the repository impl.
```

## 2. Role inventory hints (read `package.json`)

| Role | Common packages |
|---|---|
| Delivery / web framework | `@nestjs/*` / `express` / `fastify` / `koa` / `hono` |
| DI | Nest's container / `awilix` / `tsyringe` / manual factories at bootstrap |
| Database / ORM | `pg` / `knex` / `prisma` / `typeorm` / `drizzle-orm` / `mongoose` |
| Outbound HTTP | `axios` / `fetch` / `got` / `undici` |
| Validation | `zod` / `class-validator` / `joi` — belongs on delivery DTOs and data edges |
| Testing | `jest` / `vitest`; `supertest` for delivery; testcontainers or in-memory for db |

## 3. Banned imports per layer

`domain/` (entities and use cases): no web-framework imports (`express`, `@nestjs/*`
decorators), no db/ORM packages (`pg`, `prisma`, `typeorm`, `knex`), no outbound HTTP
clients, no validation libraries. Use cases may import **repository and gateway interfaces**
from `data/repositories/` (that is where they live), never anything concrete behind them:
implementations, db sources, clients, rows, or ORM entities. In Nest projects, `@Injectable()`
on use cases is the one tolerated framework touch — only if the project already does it.

Delivery (`presentation/` / `routes/` / `controllers/`): no db/ORM/SQL, no raw external
clients, no ORM entities in responses — controllers import use cases and domain types.

```bash
grep -rn "from 'express\|@nestjs/\|from 'pg\|prisma\|typeorm\|knex\|drizzle\|axios" src/features/*/domain/ && echo VIOLATION
grep -rn "from 'pg\|prisma\|typeorm\|knex\|drizzle\|SELECT \|INSERT " src/features/*/presentation/ src/**/routes/ 2>/dev/null && echo VIOLATION
```

(Adapt both globs to the project's actual layout first — a glob that matches no files prints
nothing, which reads as a false pass. ESLint `import/no-restricted-paths` is the durable form
when the project already lints.)

## 4. Composition root

Nest: the module graph (`*.module.ts`) is the composition root — providers bind contracts to
implementations. Express/Fastify: one bootstrap file (`app.ts` / `container.ts`) builds
pool/clients → sources → repository implementations (typed as the interfaces) → use cases →
routers, and nothing else constructs them.

## 5. Test idiom

`npm test` (jest/vitest). Domain and use-case tests are pure unit tests with fake
repositories (plain objects). Delivery tests are thin `supertest` runs against routes with
faked use cases, asserting status-code mapping. Repository integration tests use an
in-memory/testcontainer database per project habit. No live services for business behavior.

## Greenfield fallbacks (no project convention found)

- Layout: `src/features/<feature>/{presentation,domain,data}` (Nest projects: the existing
  `modules/<feature>` convention wins) — the repository interface and its impl both sit in
  `data/repositories/`.
- Result/error idiom: a discriminated union or small `AppError` set in `core/`; technical
  errors (`pg` errors, timeouts, 4xx/5xx from outbound calls) are translated in `data/`;
  delivery maps application errors to status codes in one place.
- Delivery: keep handlers thin — validate input (project's validator), call the use case,
  map the result. No SQL, no fetch, no business `if`s in a handler.
- Use-case naming: `VerbNounUseCase` class with `execute(…)` (or the project's factory-fn
  idiom).
