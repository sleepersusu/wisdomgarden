from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Coupon:
    expiry: date
    threshold: Decimal
    discount: Decimal
