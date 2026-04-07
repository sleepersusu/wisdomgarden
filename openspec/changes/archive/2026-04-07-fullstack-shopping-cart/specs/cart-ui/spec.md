## ADDED Requirements

### Requirement: Cart page allows building and submitting a cart
CartView SHALL allow users to set settlement date, add items, add promotions, set coupon, see live subtotal, and submit checkout.

#### Scenario: Add item and see subtotal update
- **WHEN** user selects a product and enters qty and unit price
- **THEN** live subtotal updates immediately in cartStore

#### Scenario: Submit checkout
- **WHEN** user clicks checkout button
- **THEN** POST /api/checkouts is called and success shows total amount

### Requirement: Cart state is managed by Pinia cartStore
cartStore SHALL hold items, promotions, coupon, settledAt and expose checkout() action.

#### Scenario: checkout action calls API
- **WHEN** cartStore.checkout() is called
- **THEN** API is called with current cart state and order is returned
