# Shopping Cart Design

Date: 2026-04-07  
Status: Approved

---

## Problem

實作電商購物車結算系統：讀取購物清單、當日促銷折扣、優惠券資訊，輸出實際應付金額。

---

## Approach

方案 B 精簡版：OOP 分層 + dataclass，不加 Protocol 抽象（題目只有一種促銷類型，Protocol 屬過度設計）。

---

## Directory Structure

```
shopping_cart/
├── domain/
│   ├── category.py       # Category enum
│   ├── product.py        # Product dataclass + CATALOG
│   ├── cart_item.py      # CartItem dataclass
│   ├── promotion.py      # Promotion dataclass
│   └── coupon.py         # Coupon dataclass
├── cart.py               # Cart dataclass（聚合根）
├── calculator.py         # CartCalculator.calculate(cart) -> Decimal
├── parser.py             # InputParser.parse(text) -> Cart
└── main.py               # stdin -> stdout 入口
tests/
├── unit/
│   ├── test_domain.py
│   ├── test_calculator.py
│   └── test_parser.py
└── integration/
    └── test_cases.py
pyproject.toml
```

---

## Domain Model

### Category（enum）
```
電子 | 食品 | 日用品 | 酒類
```

### CATALOG（靜態映射）
```
電子:  ipad, iphone, 顯示器, 筆記型電腦, 鍵盤
食品:  麵包, 餅乾, 蛋糕, 牛肉, 魚, 蔬菜
日用品: 餐巾紙, 收納箱, 咖啡杯, 雨傘
酒類:  啤酒, 白酒, 伏特加
```

### Promotion（dataclass, frozen）
- `date: date`
- `discount_rate: Decimal`
- `category: Category`

### Coupon（dataclass, frozen）
- `expiry: date`
- `threshold: Decimal`
- `discount: Decimal`

### CartItem（dataclass, frozen）
- `product: Product`
- `qty: int`
- `unit_price: Decimal`

### Cart（dataclass）
- `items: list[CartItem]`
- `promotions: list[Promotion]`
- `coupon: Coupon | None`
- `settlement_date: date`

---

## Calculation Logic

```
for each CartItem:
    subtotal = qty × unit_price
    find first Promotion where:
        promo.date == settlement_date AND promo.category == item.product.category
    if found: subtotal × promo.discount_rate

total = sum(subtotals)

if coupon exists
   AND settlement_date <= coupon.expiry
   AND total >= coupon.threshold:
    total -= coupon.discount

return round(total, 2)  # ROUND_HALF_UP
```

---

## Input Parsing

行型別以 regex 判斷（不依賴空行順序）：

| Pattern | 型別 |
|---------|------|
| `\d{4}\.\d+\.\d+\|\d+\.?\d*\|.+` | Promotion |
| `\d+\*.+:\d+\.?\d*` | CartItem |
| `\d{4}\.\d+\.\d+\s+\d+\s+\d+` | Coupon |
| `\d{4}\.\d+\.\d+` | settlement_date |
| 空行 / `//` 開頭 | 忽略 |

每行先截斷 `//` 後的部分再 match。  
所有數值以 `Decimal(str)` 建立，避免 float 誤差。

---

## Error Handling

| 情況 | 處理 |
|------|------|
| 商品不在 CATALOG | raise `UnknownProductError` |
| 促銷日期 ≠ 結算日期 | 不生效 |
| 優惠券過期 | 忽略 |
| 總額未達優惠券門檻 | 不扣抵 |
| 無促銷 / 無優惠券 | 正常支援 |

---

## Testing Strategy

- **Unit:** domain 模型、calculator 各情境、parser 各行格式
- **Integration:** Case A（含促銷+優惠券）、Case B（無促銷無優惠券）
- **Coverage:** line ≥ 80%、branch ≥ 80%

---

## Non-Goals

- 多張優惠券選擇
- 促銷疊加
- 負數數量
- 題目未描述的其他場景
