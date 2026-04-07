## 1. 專案骨架建立

- [x] 1.1 建立 `pyproject.toml`（pytest、pytest-cov 設定，coverage ≥ 80%）
- [x] 1.2 建立目錄結構：`shopping_cart/domain/`、`tests/unit/`、`tests/integration/`
- [x] 1.3 建立所有 `__init__.py`

## 2. Domain 模型（TDD）

- [x] 2.1 `category.py`：Category enum（ELECTRONICS / FOOD / DAILY / ALCOHOL）
- [x] 2.2 `product.py`：Product dataclass + CATALOG dict（20 項商品）
- [x] 2.3 `cart_item.py`：CartItem dataclass（product, qty, unit_price: Decimal）
- [x] 2.4 `promotion.py`：Promotion dataclass（date, discount_rate: Decimal, category）
- [x] 2.5 `coupon.py`：Coupon dataclass（expiry, threshold: Decimal, discount: Decimal）
- [x] 2.6 `cart.py`：Cart dataclass（items, promotions, coupon, settlement_date）

## 3. CartCalculator（TDD）

- [x] 3.1 先寫 `tests/unit/test_calculator.py`（無促銷、有折扣、優惠券各情境）
- [x] 3.2 實作 `calculator.py`：CartCalculator.calculate(cart) -> Decimal
- [x] 3.3 確認所有 calculator 測試通過

## 4. InputParser（TDD）

- [x] 4.1 先寫 `tests/unit/test_parser.py`（各行格式、行內註解、UnknownProductError）
- [x] 4.2 實作 `parser.py`：InputParser.parse(text) -> Cart
- [x] 4.3 確認所有 parser 測試通過

## 5. 整合測試與入口

- [x] 5.1 寫 `tests/integration/test_cases.py`：Case A（3083.60）、Case B（43.54）
- [x] 5.2 實作 `main.py`：讀取 stdin → InputParser → CartCalculator → 輸出
- [x] 5.3 確認端對端測試通過

## 6. 驗收

- [x] 6.1 執行 `pytest --cov=shopping_cart --cov-report=term-missing --cov-fail-under=80`
- [x] 6.2 確認 line ≥ 80%、branch ≥ 80%（實際 89.93%）
- [x] 6.3 手動驗證 Case A / Case B 輸出
