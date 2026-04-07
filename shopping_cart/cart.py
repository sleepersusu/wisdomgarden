from dataclasses import dataclass, field
from datetime import date

from shopping_cart.domain.cart_item import CartItem
from shopping_cart.domain.coupon import Coupon
from shopping_cart.domain.promotion import Promotion


@dataclass
class Cart:
    items: list[CartItem]
    promotions: list[Promotion]
    coupon: Coupon | None
    settlement_date: date
