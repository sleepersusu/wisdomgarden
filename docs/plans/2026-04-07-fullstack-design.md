# Fullstack Shopping Cart Design

Date: 2026-04-07  
Status: Approved

---

## Architecture

Monorepo. Backend imports existing `shopping_cart` package directly.

```
wisdomgarden/
├── shopping_cart/     # existing Python core logic
├── backend/           # FastAPI + SQLite
├── frontend/          # Vue 3 + Vite + Pinia
└── tests/             # existing core tests
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/catalog` | All products with category |
| POST | `/api/checkouts` | Checkout cart → persist → return total |
| GET | `/api/orders` | Paginated order list |
| GET | `/api/orders/{id}` | Single order with full detail |

## DB Schema (SQLite)

- `orders`: id, settled_at, total_amount, created_at
- `order_items`: id, order_id, product_key, qty, unit_price
- `order_promotions`: id, order_id, promo_date, discount_rate, category
- `order_coupon`: id, order_id (UNIQUE), expiry, threshold, discount

## Frontend Pages

- `/` — CartView: product selector, promotion rows, coupon, live subtotal, checkout CTA
- `/orders` — OrdersView: paginated order list with expandable detail

## Design System

- Colors: Primary #0891B2, CTA #22C55E, BG #ECFEFF, Text #164E63
- Fonts: Rubik (heading) + Nunito Sans (body)
- Icons: Lucide Vue
- Style: Clean modern, bold hover, 200ms transition

## Testing

- Backend: pytest + httpx, in-memory SQLite for integration tests, coverage ≥ 80%
- Frontend: Vitest, mock API, test Pinia store logic

## Build

```bash
cd backend && uvicorn app.main:app --reload --port 8000
cd frontend && npm run dev   # proxy /api → :8000
```
