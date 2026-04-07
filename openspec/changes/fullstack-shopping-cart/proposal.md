## Why

The existing shopping cart is a CLI-only tool. A web interface is needed so users can interactively build carts, checkout, and review order history through a browser.

## What Changes

- New `backend/` FastAPI service wrapping existing `shopping_cart` core logic
- New `frontend/` Vue 3 + Vite + Pinia SPA
- SQLite persistence for orders, items, promotions, and coupons
- REST API: catalog, checkout, orders

## Capabilities

### New Capabilities

- `catalog-api`: GET /api/catalog — serve product list from CATALOG
- `checkout-api`: POST /api/checkouts — calculate via existing core, persist to DB, return total
- `orders-api`: GET /api/orders + GET /api/orders/{id} — order history with full detail
- `cart-ui`: Vue frontend — CartView with product/promotion/coupon input and live subtotal
- `orders-ui`: Vue frontend — OrdersView with paginated history and expandable detail

### Modified Capabilities

## Impact

- New `backend/` directory (FastAPI app, SQLAlchemy models, repositories, services, routers)
- New `frontend/` directory (Vue 3, Vite, Pinia, Vue Router, Lucide icons)
- No changes to existing `shopping_cart/` core or `tests/`
