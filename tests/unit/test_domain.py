from datetime import date
from decimal import Decimal


# ── Category ──────────────────────────────────────────────────────────────────

def test_category_has_four_values():
    from shopping_cart.domain.category import Category
    assert len(Category) == 4


def test_category_members_exist():
    from shopping_cart.domain.category import Category
    assert Category.ELECTRONICS
    assert Category.FOOD
    assert Category.DAILY
    assert Category.ALCOHOL


# ── Product / CATALOG ─────────────────────────────────────────────────────────

def test_catalog_contains_eighteen_products():
    from shopping_cart.domain.product import CATALOG
    assert len(CATALOG) == 18


def test_electronics_products_map_to_correct_category():
    from shopping_cart.domain.category import Category
    from shopping_cart.domain.product import CATALOG
    for key in ["ipad", "iphone", "monitor", "laptop", "keyboard"]:
        assert CATALOG[key].category == Category.ELECTRONICS


def test_food_products_map_to_correct_category():
    from shopping_cart.domain.category import Category
    from shopping_cart.domain.product import CATALOG
    for key in ["bread", "biscuit", "cake", "beef", "fish", "vegetable"]:
        assert CATALOG[key].category == Category.FOOD


def test_daily_products_map_to_correct_category():
    from shopping_cart.domain.category import Category
    from shopping_cart.domain.product import CATALOG
    for key in ["napkin", "storage-box", "coffee-cup", "umbrella"]:
        assert CATALOG[key].category == Category.DAILY


def test_alcohol_products_map_to_correct_category():
    from shopping_cart.domain.category import Category
    from shopping_cart.domain.product import CATALOG
    for key in ["beer", "baijiu", "vodka"]:
        assert CATALOG[key].category == Category.ALCOHOL


def test_catalog_does_not_contain_unknown_key():
    from shopping_cart.domain.product import CATALOG
    assert CATALOG.get("unknown") is None


def test_input_name_map_covers_all_catalog_keys():
    from shopping_cart.domain.product import CATALOG, INPUT_NAME_MAP
    assert set(INPUT_NAME_MAP.values()) == set(CATALOG.keys())


def test_input_category_map_covers_all_categories():
    from shopping_cart.domain.category import Category
    from shopping_cart.domain.product import INPUT_CATEGORY_MAP
    assert set(INPUT_CATEGORY_MAP.values()) == set(Category)


# ── CartItem ──────────────────────────────────────────────────────────────────

def test_cart_item_stores_qty_and_price():
    from shopping_cart.domain.cart_item import CartItem
    from shopping_cart.domain.product import CATALOG
    item = CartItem(product=CATALOG["ipad"], qty=2, unit_price=Decimal("2399.00"))
    assert item.qty == 2
    assert item.unit_price == Decimal("2399.00")
    assert item.product.name == "ipad"


# ── Promotion ─────────────────────────────────────────────────────────────────

def test_promotion_stores_date_discount_rate_and_category():
    from shopping_cart.domain.category import Category
    from shopping_cart.domain.promotion import Promotion
    promo = Promotion(
        date=date(2015, 11, 11),
        discount_rate=Decimal("0.7"),
        category=Category.ELECTRONICS,
    )
    assert promo.date == date(2015, 11, 11)
    assert promo.discount_rate == Decimal("0.7")
    assert promo.category == Category.ELECTRONICS


# ── Coupon ────────────────────────────────────────────────────────────────────

def test_coupon_stores_expiry_threshold_and_discount():
    from shopping_cart.domain.coupon import Coupon
    coupon = Coupon(
        expiry=date(2016, 3, 2),
        threshold=Decimal("1000"),
        discount=Decimal("200"),
    )
    assert coupon.expiry == date(2016, 3, 2)
    assert coupon.threshold == Decimal("1000")
    assert coupon.discount == Decimal("200")


# ── Cart ──────────────────────────────────────────────────────────────────────

def test_cart_holds_items_promotions_coupon_and_settlement_date():
    from shopping_cart.cart import Cart
    from shopping_cart.domain.cart_item import CartItem
    from shopping_cart.domain.product import CATALOG
    item = CartItem(product=CATALOG["ipad"], qty=1, unit_price=Decimal("2399.00"))
    cart = Cart(
        items=[item],
        promotions=[],
        coupon=None,
        settlement_date=date(2015, 11, 11),
    )
    assert len(cart.items) == 1
    assert cart.coupon is None
    assert cart.settlement_date == date(2015, 11, 11)
