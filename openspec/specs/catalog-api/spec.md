# catalog-api Specification

## Purpose
TBD - created by archiving change fullstack-shopping-cart. Update Purpose after archive.
## Requirements
### Requirement: Catalog endpoint returns all products
GET /api/catalog SHALL return all products from CATALOG with their English key, display name, and category.

#### Scenario: Catalog response
- **WHEN** GET /api/catalog
- **THEN** response 200 with array of 18 products each having key, display_name, category

