## Context

全新購物車結算系統，從零開始建立。Python 純函式庫，無外部依賴，stdin/stdout 介面。

## Goals / Non-Goals

**Goals:**
- 正確計算促銷折扣（日期+品類匹配）與優惠券扣抵
- OOP 分層設計：domain models / Cart / CartCalculator / InputParser
- TDD 實作，line & branch coverage ≥ 80%
- 使用 `Decimal` 避免浮點誤差

**Non-Goals:**
- 多張優惠券疊加
- 動態商品目錄（CATALOG 靜態定義即可）
- Web API / 資料庫 / 非同步

## Decisions

| 決策 | 選擇 | 理由 |
|------|------|------|
| 金額型別 | `Decimal` | 避免 float 累積誤差，四捨五入結果準確 |
| Promotion 抽象 | dataclass（非 Protocol） | 題目只有一種促銷類型，Protocol 屬過度設計 |
| 行格式識別 | regex（不依賴空行位置） | 輸入格式有時省略空行，regex 更穩健 |
| 商品目錄 | 靜態 dict CATALOG | 題目明確列出全部品項，不需動態查詢 |
| 測試分層 | unit + integration | unit 覆蓋各情境，integration 驗證 Case A/B |

**模組結構：**
```
shopping_cart/
├── domain/
│   ├── category.py     # Category enum
│   ├── product.py      # Product dataclass + CATALOG
│   ├── cart_item.py    # CartItem dataclass
│   ├── promotion.py    # Promotion dataclass
│   └── coupon.py       # Coupon dataclass
├── cart.py             # Cart dataclass（聚合根）
├── calculator.py       # CartCalculator.calculate(cart) -> Decimal
├── parser.py           # InputParser.parse(text) -> Cart
└── main.py             # stdin -> stdout 入口
```

**結算流程：**
```
for each CartItem:
    subtotal = qty × unit_price
    match first Promotion: promo.date == settlement_date AND promo.category == item.category
    if match: subtotal × promo.discount_rate
total = Σ subtotals
if coupon valid AND total >= threshold: total -= coupon.discount
return Decimal(total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

## Risks / Trade-offs

- CATALOG 硬編碼：未來新增商品需改程式碼，但題目範圍固定，可接受
- 單一促銷 match（取第一筆）：題目無促銷疊加需求，簡單策略足夠
