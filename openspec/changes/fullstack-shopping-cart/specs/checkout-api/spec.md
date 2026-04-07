## ADDED Requirements

### Requirement: Checkout endpoint persists and returns total
POST /api/checkouts SHALL accept cart data, calculate total via CartCalculator, persist full record to SQLite, and return the order with total_amount.

#### Scenario: Valid checkout request
- **WHEN** POST /api/checkouts with valid items, promotions, coupon, settled_at
- **THEN** response 201 with order id and total_amount

#### Scenario: Unknown product in items
- **WHEN** POST /api/checkouts with product_name not in CATALOG
- **THEN** response 422 with VALIDATION_FAILED error code

#### Scenario: No coupon
- **WHEN** POST /api/checkouts with coupon: null
- **THEN** checkout succeeds without coupon deduction
