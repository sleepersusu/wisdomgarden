import re
from datetime import date
from decimal import Decimal

from shopping_cart.cart import Cart
from shopping_cart.domain.cart_item import CartItem
from shopping_cart.domain.coupon import Coupon
from shopping_cart.domain.product import CATALOG, INPUT_CATEGORY_MAP, INPUT_NAME_MAP
from shopping_cart.domain.promotion import Promotion

_PROMOTION_RE = re.compile(r"^(\d{4}\.\d+\.\d+)\|(\d+(?:\.\d+)?)\|(.+)$")
_ITEM_RE = re.compile(r"^(\d+)\*(.+):(\d+(?:\.\d+)?)$")
_COUPON_RE = re.compile(r"^(\d{4}\.\d+\.\d+)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)$")
_DATE_RE = re.compile(r"^\d{4}\.\d+\.\d+$")


class UnknownProductError(ValueError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown product: {name!r}")
        self.name = name


def _parse_date(token: str) -> date:
    parts = token.split(".")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


class InputParser:
    @staticmethod
    def parse(text: str) -> Cart:
        promotions: list[Promotion] = []
        items: list[CartItem] = []
        settlement_date: date | None = None
        coupon: Coupon | None = None

        for raw in text.splitlines():
            line = raw.split("//")[0].strip()
            if not line:
                continue

            if m := _PROMOTION_RE.match(line):
                category = INPUT_CATEGORY_MAP[m.group(3).strip()]
                promotions.append(
                    Promotion(
                        date=_parse_date(m.group(1)),
                        discount_rate=Decimal(m.group(2)),
                        category=category,
                    )
                )
            elif m := _ITEM_RE.match(line):
                input_name = m.group(2).strip()
                catalog_key = INPUT_NAME_MAP.get(input_name)
                if catalog_key is None:
                    raise UnknownProductError(input_name)
                items.append(
                    CartItem(
                        product=CATALOG[catalog_key],
                        qty=int(m.group(1)),
                        unit_price=Decimal(m.group(3)),
                    )
                )
            elif m := _COUPON_RE.match(line):
                coupon = Coupon(
                    expiry=_parse_date(m.group(1)),
                    threshold=Decimal(m.group(2)),
                    discount=Decimal(m.group(3)),
                )
            elif _DATE_RE.match(line):
                settlement_date = _parse_date(line)

        if settlement_date is None:
            raise ValueError("Settlement date not found in input")

        return Cart(
            items=items,
            promotions=promotions,
            coupon=coupon,
            settlement_date=settlement_date,
        )
