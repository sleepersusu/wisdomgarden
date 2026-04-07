# input-parsing Specification

## Purpose
TBD - created by archiving change shopping-cart-checkout. Update Purpose after archive.
## Requirements
### Requirement: 解析促銷行
系統 SHALL 將格式為 `YYYY.M.D|rate|category` 的行解析為 Promotion 物件。

#### Scenario: 合法促銷行
- **WHEN** 行符合 `\d{4}\.\d+\.\d+\|\d+\.?\d*\|.+` 格式
- **THEN** 建立 Promotion(date, discount_rate, category)

#### Scenario: 無促銷（空行）
- **WHEN** 行為空行
- **THEN** 忽略該行

### Requirement: 解析商品行
系統 SHALL 將格式為 `qty*name:price` 的行解析為 CartItem 物件。

#### Scenario: 合法商品行
- **WHEN** 行符合 `\d+\*.+:\d+\.?\d*` 格式
- **THEN** 建立 CartItem(product, qty, unit_price)

#### Scenario: 商品不在 CATALOG
- **WHEN** 商品名稱不存在於 CATALOG
- **THEN** raise UnknownProductError

### Requirement: 解析結算日期與優惠券
系統 SHALL 區分單獨日期行（結算日）與含數字的日期行（優惠券）。

#### Scenario: 結算日期行
- **WHEN** 行符合 `^\d{4}\.\d+\.\d+$`
- **THEN** 設為 settlement_date

#### Scenario: 優惠券行
- **WHEN** 行符合 `^\d{4}\.\d+\.\d+\s+\d+\s+\d+$`
- **THEN** 建立 Coupon(expiry, threshold, discount)

### Requirement: 忽略行內註解
系統 SHALL 截斷每行 `//` 後的部分再進行解析。

#### Scenario: 行含 // 註解
- **WHEN** 行包含 `//`
- **THEN** 僅處理 `//` 之前的內容

