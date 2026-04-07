# product-catalog Specification

## Purpose
TBD - created by archiving change shopping-cart-checkout. Update Purpose after archive.
## Requirements
### Requirement: 靜態商品目錄 CATALOG
系統 SHALL 提供靜態 CATALOG dict，映射商品名稱至 Product（含 Category）。

#### Scenario: 查詢已知商品
- **WHEN** 以已知商品名稱查詢 CATALOG
- **THEN** 回傳對應 Product 及其 Category

#### Scenario: 查詢未知商品
- **WHEN** 商品名稱不在 CATALOG
- **THEN** 回傳 None（由 parser 決定是否 raise）

### Requirement: 支援四種品類
系統 SHALL 以 enum 定義 Category：電子、食品、日用品、酒類。

#### Scenario: Category enum 涵蓋所有品類
- **WHEN** 建立 Category enum
- **THEN** 包含 ELECTRONICS、FOOD、DAILY、ALCOHOL 四個值

### Requirement: 商品品項完整對應
系統 SHALL 覆蓋題目指定的 20 項商品。

#### Scenario: 電子品類商品
- **WHEN** 查詢 ipad / iphone / 顯示器 / 筆記型電腦 / 鍵盤
- **THEN** Category 為 ELECTRONICS

#### Scenario: 食品品類商品
- **WHEN** 查詢 麵包 / 餅乾 / 蛋糕 / 牛肉 / 魚 / 蔬菜
- **THEN** Category 為 FOOD

#### Scenario: 日用品品類商品
- **WHEN** 查詢 餐巾紙 / 收納箱 / 咖啡杯 / 雨傘
- **THEN** Category 為 DAILY

#### Scenario: 酒類品類商品
- **WHEN** 查詢 啤酒 / 白酒 / 伏特加
- **THEN** Category 為 ALCOHOL

