from datetime import date
from decimal import Decimal

import pytest

from shopping_cart.cart import Cart
from shopping_cart.domain.cart_item import CartItem
from shopping_cart.domain.category import Category
from shopping_cart.domain.coupon import Coupon
from shopping_cart.domain.product import CATALOG
from shopping_cart.domain.promotion import Promotion


def make_cart(
    items: list[CartItem],
    promotions: list[Promotion] | None = None,
    coupon: Coupon | None = None,
    settlement_date: date = date(2015, 11, 11),
) -> Cart:
    return Cart(
        items=items,
        promotions=promotions or [],
        coupon=coupon,
        settlement_date=settlement_date,
    )


# ── No discount, no coupon ─────────────────────────────────────────────────────

def test_single_item_no_promotion():
    cart = make_cart([CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))])
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2399.00")


def test_multiple_items_no_promotion():
    items = [
        CartItem(CATALOG["ipad"],      qty=1, unit_price=Decimal("2399.00")),
        CartItem(CATALOG["beer"],      qty=12, unit_price=Decimal("25.00")),
    ]
    cart = make_cart(items)
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2699.00")


# ── Promotion applies ──────────────────────────────────────────────────────────

def test_promotion_applies_when_date_and_category_match():
    promo = Promotion(date=date(2015, 11, 11), discount_rate=Decimal("0.7"), category=Category.ELECTRONICS)
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, promotions=[promo])
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("1679.30")


def test_promotion_does_not_apply_when_date_differs():
    promo = Promotion(date=date(2015, 12, 12), discount_rate=Decimal("0.7"), category=Category.ELECTRONICS)
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, promotions=[promo])
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2399.00")


def test_promotion_does_not_apply_when_category_differs():
    promo = Promotion(date=date(2015, 11, 11), discount_rate=Decimal("0.7"), category=Category.FOOD)
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, promotions=[promo])
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2399.00")


def test_promotion_applies_only_to_matching_category_items():
    promo = Promotion(date=date(2015, 11, 11), discount_rate=Decimal("0.7"), category=Category.ELECTRONICS)
    items = [
        CartItem(CATALOG["ipad"],  qty=1, unit_price=Decimal("2399.00")),
        CartItem(CATALOG["beer"],  qty=12, unit_price=Decimal("25.00")),
    ]
    cart = make_cart(items, promotions=[promo])
    from shopping_cart.calculator import CartCalculator
    # ipad: 2399 * 0.7 = 1679.30; beer: 300.00
    assert CartCalculator.calculate(cart) == Decimal("1979.30")


# ── Coupon ─────────────────────────────────────────────────────────────────────

def test_coupon_deducted_when_total_meets_threshold():
    coupon = Coupon(expiry=date(2016, 3, 2), threshold=Decimal("1000"), discount=Decimal("200"))
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, coupon=coupon)
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2199.00")


def test_coupon_not_applied_when_total_below_threshold():
    coupon = Coupon(expiry=date(2016, 3, 2), threshold=Decimal("1000"), discount=Decimal("200"))
    items = [CartItem(CATALOG["bread"], qty=1, unit_price=Decimal("9.00"))]
    cart = make_cart(items, coupon=coupon)
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("9.00")


def test_coupon_not_applied_when_expired():
    coupon = Coupon(expiry=date(2014, 1, 1), threshold=Decimal("1000"), discount=Decimal("200"))
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, coupon=coupon, settlement_date=date(2015, 11, 11))
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2399.00")


def test_no_coupon_returns_plain_total():
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, coupon=None)
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("2399.00")


# ── Rounding ───────────────────────────────────────────────────────────────────

def test_result_is_rounded_to_two_decimal_places():
    promo = Promotion(date=date(2015, 11, 11), discount_rate=Decimal("0.7"), category=Category.ELECTRONICS)
    items = [CartItem(CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))]
    cart = make_cart(items, promotions=[promo])
    from shopping_cart.calculator import CartCalculator
    result = CartCalculator.calculate(cart)
    assert result == result.quantize(Decimal("0.01"))


# ── End-to-end scenarios ───────────────────────────────────────────────────────

def test_case_a_full_scenario():
    """Case A from problem statement: expected total = 3083.60"""
    promo = Promotion(date=date(2015, 11, 11), discount_rate=Decimal("0.7"), category=Category.ELECTRONICS)
    coupon = Coupon(expiry=date(2016, 3, 2), threshold=Decimal("1000"), discount=Decimal("200"))
    items = [
        CartItem(CATALOG["ipad"],      qty=1,  unit_price=Decimal("2399.00")),
        CartItem(CATALOG["monitor"],   qty=1,  unit_price=Decimal("1799.00")),
        CartItem(CATALOG["beer"],      qty=12, unit_price=Decimal("25.00")),
        CartItem(CATALOG["bread"],     qty=5,  unit_price=Decimal("9.00")),
    ]
    cart = Cart(
        items=items,
        promotions=[promo],
        coupon=coupon,
        settlement_date=date(2015, 11, 11),
    )
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("3083.60")


def test_case_b_full_scenario():
    """Case B from problem statement: expected total = 43.54"""
    items = [
        CartItem(CATALOG["vegetable"], qty=3, unit_price=Decimal("5.98")),
        CartItem(CATALOG["napkin"],    qty=8, unit_price=Decimal("3.20")),
    ]
    cart = Cart(
        items=items,
        promotions=[],
        coupon=None,
        settlement_date=date(2015, 1, 1),
    )
    from shopping_cart.calculator import CartCalculator
    assert CartCalculator.calculate(cart) == Decimal("43.54")
