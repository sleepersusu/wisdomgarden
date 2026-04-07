## Why

電商網站需要一個購物車結算系統，能夠根據當日促銷折扣與優惠券自動計算用戶實際應付金額，目前尚無任何實作。

## What Changes

- 新增購物車結算程式，從 stdin 讀取購物清單與促銷資訊，輸出結算金額至 stdout
- 支援日期+品類促銷折扣（可多筆，結算日與促銷日相符才生效）
- 支援一次結算使用一張優惠券（滿額折抵，需在有效期內）
- 內建固定商品目錄（電子、食品、日用品、酒類共 20 項商品）

## Capabilities

### New Capabilities

- `cart-calculation`: 購物車結算邏輯（折扣 + 優惠券 + 金額加總）
- `input-parsing`: 解析文字輸入格式為領域物件
- `product-catalog`: 商品品類目錄靜態定義

### Modified Capabilities

## Impact

- 新建 `shopping_cart/` Python 套件（domain 模型、calculator、parser、main 入口）
- 新建 `tests/` 測試套件（unit + integration）
- 新建 `pyproject.toml` 定義建構與測試指令
- 無外部 API 依賴，無資料庫
