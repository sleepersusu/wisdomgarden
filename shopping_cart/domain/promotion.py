from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from shopping_cart.domain.category import Category


@dataclass(frozen=True)
class Promotion:
    date: date
    discount_rate: Decimal
    category: Category
