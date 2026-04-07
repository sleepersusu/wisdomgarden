# cart-calculation Specification

## Purpose
TBD - created by archiving change shopping-cart-checkout. Update Purpose after archive.
## Requirements
### Requirement: 計算商品小計並套用促銷折扣
系統 SHALL 對每個購物車項目計算 qty × unit_price，並在促銷日期等於結算日期且品類相符時，乘以 discount_rate。

#### Scenario: 無促銷，直接加總
- **WHEN** 購物車有商品但無任何促銷
- **THEN** 結算金額 = Σ(qty × unit_price)

#### Scenario: 促銷日期與結算日期相符，品類相符
- **WHEN** 促銷日期 == 結算日期 且商品品類與促銷品類相同
- **THEN** 該商品小計 × discount_rate

#### Scenario: 促銷日期與結算日期不符
- **WHEN** 促銷日期 ≠ 結算日期
- **THEN** 促銷不生效，以原價計算

#### Scenario: 商品品類與促銷品類不符
- **WHEN** 商品品類與促銷品類不同
- **THEN** 該商品不打折

### Requirement: 套用優惠券折抵
系統 SHALL 在優惠券有效且總金額達門檻時，從總金額扣抵 coupon.discount。

#### Scenario: 優惠券有效且達門檻
- **WHEN** settlement_date <= coupon.expiry AND total >= coupon.threshold
- **THEN** total -= coupon.discount

#### Scenario: 優惠券已過期
- **WHEN** settlement_date > coupon.expiry
- **THEN** 優惠券不生效

#### Scenario: 總金額未達門檻
- **WHEN** total < coupon.threshold
- **THEN** 優惠券不生效

#### Scenario: 無優惠券
- **WHEN** coupon 為 None
- **THEN** 直接回傳加總金額

### Requirement: 結算金額四捨五入至小數點後兩位
系統 SHALL 使用 ROUND_HALF_UP 將最終金額四捨五入至 0.01。

#### Scenario: 有小數需四捨五入
- **WHEN** 計算結果小數點第三位 >= 5
- **THEN** 進位至小數點後兩位

