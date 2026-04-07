# Shopping Cart — Logic Guide

## Overview

This program reads a shopping cart from stdin and prints the final amount the customer must pay.

```
stdin → InputParser → Cart → CartCalculator → stdout
```

---

## Input Format

Each line represents one piece of information. Lines can appear in any order; blank lines and inline `//` comments are ignored.

### Promotion Line

```
2015.11.11|0.7|電子
```

| Field | Example | Meaning |
|-------|---------|---------|
| Date | `2015.11.11` | The date this discount is active (YYYY.M.D) |
| Discount rate | `0.7` | Multiplier applied to item subtotal (0.7 = 30% off) |
| Category | `電子` | Product category that receives the discount |

Multiple promotion lines are allowed. A promotion only applies if its date matches the settlement date.

Supported categories: `電子` (Electronics), `食品` (Food), `日用品` (Daily goods), `酒類` (Alcohol)

---

### Item Line

```
1*ipad:2399.00
```

| Field | Example | Meaning |
|-------|---------|---------|
| Quantity | `1` | Number of units purchased |
| Product name | `ipad` | Must be in the supported product catalog |
| Unit price | `2399.00` | Price per unit in currency |

---

### Settlement Date Line

```
2015.11.11
```

A standalone date (no `|` and no trailing numbers). This is the date on which the cart is checked out. Promotions are matched against this date.

---

### Coupon Line

```
2016.3.2 1000 200
```

| Field | Example | Meaning |
|-------|---------|---------|
| Expiry date | `2016.3.2` | Coupon is valid up to and including this date |
| Threshold | `1000` | Minimum total required to apply the coupon |
| Discount | `200` | Amount deducted from total when threshold is met |

Only one coupon per checkout. Coupon is applied after all promotional discounts.

---

## Calculation Logic

```
for each item:
    subtotal = qty × unit_price

    find first promotion where:
        promotion.date == settlement_date
        promotion.category == item.category

    if found:
        subtotal = subtotal × promotion.discount_rate

total = sum of all subtotals

if coupon exists
   AND settlement_date <= coupon.expiry
   AND total >= coupon.threshold:
    total = total - coupon.discount

output = round(total, 2 decimal places, ROUND_HALF_UP)
```

---

## Product Catalog

| Category | Internal key | Input name (Chinese) |
|----------|-------------|----------------------|
| Electronics | `ipad` | ipad |
| Electronics | `iphone` | iphone |
| Electronics | `monitor` | 顯示器 |
| Electronics | `laptop` | 筆記型電腦 |
| Electronics | `keyboard` | 鍵盤 |
| Food | `bread` | 麵包 |
| Food | `biscuit` | 餅乾 |
| Food | `cake` | 蛋糕 |
| Food | `beef` | 牛肉 |
| Food | `fish` | 魚 |
| Food | `vegetable` | 蔬菜 |
| Daily | `napkin` | 餐巾紙 |
| Daily | `storage-box` | 收納箱 |
| Daily | `coffee-cup` | 咖啡杯 |
| Daily | `umbrella` | 雨傘 |
| Alcohol | `beer` | 啤酒 |
| Alcohol | `baijiu` | 白酒 |
| Alcohol | `vodka` | 伏特加 |

---

## Worked Examples

### Case A — Electronics promotion + coupon

**Input:**
```
2015.11.11|0.7|電子
1*ipad:2399.00
1*顯示器:1799.00
12*啤酒:25.00
5*麵包:9.00
2015.11.11
2016.3.2 1000 200
```

**Step-by-step:**

| Item | qty × price | Promotion | Subtotal |
|------|------------|-----------|---------|
| ipad | 1 × 2399.00 | ×0.7 (Electronics, date matches) | 1679.30 |
| 顯示器 | 1 × 1799.00 | ×0.7 (Electronics, date matches) | 1259.30 |
| 啤酒 | 12 × 25.00 | none (Alcohol, not Electronics) | 300.00 |
| 麵包 | 5 × 9.00 | none (Food, not Electronics) | 45.00 |

Sum before coupon: **3283.60**

Coupon check: settlement date 2015.11.11 ≤ expiry 2016.3.2 ✓, total 3283.60 ≥ threshold 1000 ✓
→ Deduct 200

**Output: `3083.60`**

---

### Case B — No promotion, no coupon

**Input:**
```
3*蔬菜:5.98
8*餐巾紙:3.20
2015.01.01
```

| Item | qty × price | Subtotal |
|------|------------|---------|
| 蔬菜 | 3 × 5.98 | 17.94 |
| 餐巾紙 | 8 × 3.20 | 25.60 |

**Output: `43.54`**

---

## Running the Program

```bash
# Run with stdin input
echo "1*ipad:2399.00
2015.11.11" | python -m shopping_cart.main

# Run all tests with coverage
python -m pytest --cov=shopping_cart --cov-report=term-missing --cov-fail-under=80
```

---

## Module Reference

| Module | Responsibility |
|--------|---------------|
| `shopping_cart/domain/category.py` | `Category` enum — four product categories |
| `shopping_cart/domain/product.py` | `Product` dataclass, `CATALOG` (English keys), `INPUT_NAME_MAP` (Chinese → key), `INPUT_CATEGORY_MAP` (Chinese → Category) |
| `shopping_cart/domain/cart_item.py` | `CartItem(product, qty, unit_price)` — one line item |
| `shopping_cart/domain/promotion.py` | `Promotion(date, discount_rate, category)` — one discount rule |
| `shopping_cart/domain/coupon.py` | `Coupon(expiry, threshold, discount)` — one-time voucher |
| `shopping_cart/cart.py` | `Cart(items, promotions, coupon, settlement_date)` — aggregate |
| `shopping_cart/calculator.py` | `CartCalculator.calculate(cart)` — pure calculation, returns `Decimal` |
| `shopping_cart/parser.py` | `InputParser.parse(text)` — converts raw text to `Cart` |
| `shopping_cart/main.py` | Entry point: stdin → parse → calculate → stdout |
