from dataclasses import dataclass
from decimal import Decimal

from shopping_cart.domain.product import Product


@dataclass(frozen=True)
class CartItem:
    product: Product
    qty: int
    unit_price: Decimal
