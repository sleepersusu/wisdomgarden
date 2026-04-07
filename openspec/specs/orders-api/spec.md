# orders-api Specification

## Purpose
TBD - created by archiving change fullstack-shopping-cart. Update Purpose after archive.
## Requirements
### Requirement: List orders with pagination
GET /api/orders SHALL return paginated list of orders sorted by created_at descending.

#### Scenario: Default pagination
- **WHEN** GET /api/orders
- **THEN** response 200 with items array and pagination metadata (page, size, total_elements, total_pages)

### Requirement: Get single order with full detail
GET /api/orders/{order_id} SHALL return order with items, promotions, and coupon.

#### Scenario: Existing order
- **WHEN** GET /api/orders/{id} with valid id
- **THEN** response 200 with full order detail including items and promotions

#### Scenario: Non-existent order
- **WHEN** GET /api/orders/{id} with unknown id
- **THEN** response 404 with ORDER_NOT_FOUND error code

