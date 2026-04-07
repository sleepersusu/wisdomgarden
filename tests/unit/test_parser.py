from datetime import date
from decimal import Decimal

import pytest


# ── Promotion parsing ──────────────────────────────────────────────────────────

def test_parses_promotion_line():
    from shopping_cart.domain.category import Category
    from shopping_cart.parser import InputParser
    cart = InputParser.parse("2015.11.11|0.7|電子\n1*ipad:2399.00\n2015.11.11")
    assert len(cart.promotions) == 1
    assert cart.promotions[0].date == date(2015, 11, 11)
    assert cart.promotions[0].discount_rate == Decimal("0.7")
    assert cart.promotions[0].category == Category.ELECTRONICS


def test_parses_multiple_promotion_lines():
    from shopping_cart.parser import InputParser
    text = "2015.11.11|0.7|電子\n2015.11.11|0.9|食品\n1*ipad:2399.00\n2015.11.11"
    cart = InputParser.parse(text)
    assert len(cart.promotions) == 2


# ── Item parsing ───────────────────────────────────────────────────────────────

def test_parses_single_item():
    from shopping_cart.parser import InputParser
    cart = InputParser.parse("1*ipad:2399.00\n2015.11.11")
    assert len(cart.items) == 1
    assert cart.items[0].qty == 1
    assert cart.items[0].unit_price == Decimal("2399.00")
    assert cart.items[0].product.name == "ipad"


def test_parses_multiple_items():
    from shopping_cart.parser import InputParser
    text = "1*ipad:2399.00\n12*啤酒:25.00\n2015.11.11"
    cart = InputParser.parse(text)
    assert len(cart.items) == 2
    assert cart.items[1].qty == 12


def test_raises_for_unknown_product():
    from shopping_cart.parser import InputParser, UnknownProductError
    with pytest.raises(UnknownProductError):
        InputParser.parse("1*unknown-product:99.00\n2015.11.11")


# ── Settlement date parsing ────────────────────────────────────────────────────

def test_parses_settlement_date():
    from shopping_cart.parser import InputParser
    cart = InputParser.parse("1*ipad:2399.00\n2015.11.11")
    assert cart.settlement_date == date(2015, 11, 11)


def test_parses_single_digit_month_and_day():
    from shopping_cart.parser import InputParser
    cart = InputParser.parse("1*ipad:2399.00\n2015.1.1")
    assert cart.settlement_date == date(2015, 1, 1)


# ── Coupon parsing ─────────────────────────────────────────────────────────────

def test_parses_coupon_line():
    from shopping_cart.parser import InputParser
    cart = InputParser.parse("1*ipad:2399.00\n2015.11.11\n2016.3.2 1000 200")
    assert cart.coupon is not None
    assert cart.coupon.expiry == date(2016, 3, 2)
    assert cart.coupon.threshold == Decimal("1000")
    assert cart.coupon.discount == Decimal("200")


def test_no_coupon_when_absent():
    from shopping_cart.parser import InputParser
    cart = InputParser.parse("1*ipad:2399.00\n2015.11.11")
    assert cart.coupon is None


# ── Comment stripping ──────────────────────────────────────────────────────────

def test_strips_inline_comments():
    from shopping_cart.parser import InputParser
    text = "1*ipad:2399.00 //some comment\n2015.11.11 //another comment"
    cart = InputParser.parse(text)
    assert len(cart.items) == 1
    assert cart.settlement_date == date(2015, 11, 11)


def test_ignores_comment_only_lines():
    from shopping_cart.parser import InputParser
    text = "//this is a comment\n1*ipad:2399.00\n2015.11.11"
    cart = InputParser.parse(text)
    assert len(cart.items) == 1


# ── Full input (Case A) ────────────────────────────────────────────────────────

def test_parses_case_a_input_completely():
    from shopping_cart.domain.category import Category
    from shopping_cart.parser import InputParser
    text = (
        "2015.11.11|0.7|電子 //promotion\n"
        "\n"
        "1*ipad:2399.00\n"
        "1*顯示器:1799.00\n"
        "12*啤酒:25.00\n"
        "5*麵包:9.00\n"
        "\n"
        "2015.11.11 //settlement date\n"
        "2016.3.2 1000 200 //coupon\n"
    )
    cart = InputParser.parse(text)
    assert cart.settlement_date == date(2015, 11, 11)
    assert len(cart.promotions) == 1
    assert cart.promotions[0].category == Category.ELECTRONICS
    assert len(cart.items) == 4
    assert cart.coupon is not None
    assert cart.coupon.discount == Decimal("200")
