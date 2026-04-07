## Context

Monorepo. Backend imports `shopping_cart` package. Frontend proxies `/api` to FastAPI on port 8000.

## Goals / Non-Goals

**Goals:**
- REST API wrapping existing calculation logic
- SQLite persistence (full order record: items + promotions + coupon)
- Vue SPA: cart input page + order history page
- Backend coverage ≥ 80%, Vitest for Pinia stores

**Non-Goals:**
- Auth / user accounts
- Real payment processing
- SSR / production deployment

## Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| DB | SQLite via SQLAlchemy sync | Lightweight, zero setup, matches requirement |
| ORM | SQLAlchemy 2.0 (sync) | Simpler than async for SQLite; no real concurrency need |
| Validation | Pydantic v2 | Already in project rules |
| Frontend state | Pinia | Required by spec |
| Frontend validation | Native HTML5 | No complex forms; VeeValidate is overkill |
| Icons | Lucide Vue | Consistent SVG set |

## Risks / Trade-offs

- Sync SQLAlchemy: fine for SQLite single-user demo, not production-scale
- No auth: acceptable for interview/demo scope
