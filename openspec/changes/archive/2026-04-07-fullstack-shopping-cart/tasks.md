## 1. Backend Scaffold

- [ ] 1.1 建立 `backend/` 目錄結構與 `pyproject.toml`（fastapi, sqlalchemy, uvicorn, httpx, pytest-cov）
- [ ] 1.2 `backend/app/core/database.py`：SQLite engine + session factory + `get_session` dependency
- [ ] 1.3 `backend/app/core/exceptions.py`：AppError, OrderNotFoundError, exception handler
- [ ] 1.4 `backend/app/main.py`：FastAPI app，掛載 routers，CORS

## 2. ORM Models

- [ ] 2.1 `backend/app/models/order.py`：Order, OrderItem, OrderPromotion, OrderCoupon（SQLAlchemy 2.0）
- [ ] 2.2 建立 `create_tables()` 在 startup event 自動建表

## 3. Schemas

- [ ] 3.1 `backend/app/schemas/checkout.py`：CheckoutRequest, ItemIn, PromotionIn, CouponIn
- [ ] 3.2 `backend/app/schemas/order.py`：OrderResponse, OrderDetailResponse, PaginatedOrdersResponse

## 4. Catalog API（TDD）

- [ ] 4.1 先寫 `backend/tests/integration/test_catalog.py`（GET /api/catalog → 18 items）
- [ ] 4.2 實作 `backend/app/routers/catalog.py`
- [ ] 4.3 確認測試通過

## 5. Checkout API（TDD）

- [ ] 5.1 先寫 `backend/tests/integration/test_checkout.py`（成功、未知商品）
- [ ] 5.2 實作 `backend/app/repositories/order_repository.py`
- [ ] 5.3 實作 `backend/app/services/checkout_service.py`（呼叫 shopping_cart core）
- [ ] 5.4 實作 `backend/app/routers/checkout.py`
- [ ] 5.5 確認測試通過

## 6. Orders API（TDD）

- [ ] 6.1 先寫 `backend/tests/integration/test_orders.py`（list、detail、404）
- [ ] 6.2 實作 `backend/app/routers/orders.py`
- [ ] 6.3 確認測試通過

## 7. Frontend Scaffold

- [ ] 7.1 `npm create vite@latest frontend -- --template vue-ts`
- [ ] 7.2 安裝 pinia、vue-router、lucide-vue-next
- [ ] 7.3 設定 `vite.config.ts` proxy `/api → localhost:8000`
- [ ] 7.4 設定 Google Fonts（Rubik + Nunito Sans）、global CSS 變數

## 8. Pinia Stores（TDD with Vitest）

- [ ] 8.1 先寫 `frontend/src/stores/__tests__/cartStore.test.ts`
- [ ] 8.2 實作 `frontend/src/stores/cartStore.ts`
- [ ] 8.3 先寫 `frontend/src/stores/__tests__/orderStore.test.ts`
- [ ] 8.4 實作 `frontend/src/stores/orderStore.ts`
- [ ] 8.5 確認 Vitest 通過

## 9. Frontend Components & Views

- [ ] 9.1 `frontend/src/router/index.ts`：/ 和 /orders 路由
- [ ] 9.2 `frontend/src/App.vue`：navbar + router-view
- [ ] 9.3 `frontend/src/views/CartView.vue`（含 ProductSelector, PromotionInput, CouponInput, CartSummary）
- [ ] 9.4 `frontend/src/views/OrdersView.vue`（含 OrderDetail 展開）

## 10. Verification

- [ ] 10.1 `cd backend && pytest --cov=app --cov-fail-under=80`
- [ ] 10.2 `cd frontend && npm run test`
- [ ] 10.3 手動測試：Case A checkout → 3083.60，訂單歷史顯示
