from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order, OrderCoupon, OrderItem, OrderPromotion
from app.repositories.order_repository import OrderRepository
from app.schemas.checkout import CheckoutRequest
from shopping_cart.cart import Cart
from shopping_cart.calculator import CartCalculator
from shopping_cart.domain.cart_item import CartItem
from shopping_cart.domain.category import Category
from shopping_cart.domain.coupon import Coupon
from shopping_cart.domain.product import CATALOG, INPUT_CATEGORY_MAP
from shopping_cart.domain.promotion import Promotion
from shopping_cart.parser import UnknownProductError


class CheckoutService:
    def __init__(self, session: Session) -> None:
        self._repo = OrderRepository(session)

    def checkout(self, request: CheckoutRequest) -> Order:
        cart = self._build_cart(request)
        total = CartCalculator.calculate(cart)

        order = Order(settled_at=request.settled_at, total_amount=float(total))

        for item_in in request.items:
            order.items.append(
                OrderItem(
                    product_key=item_in.product_name,
                    qty=item_in.qty,
                    unit_price=item_in.unit_price,
                )
            )

        for promo_in in request.promotions:
            order.promotions.append(
                OrderPromotion(
                    promo_date=promo_in.date,
                    discount_rate=promo_in.discount_rate,
                    category=promo_in.category,
                )
            )

        if request.coupon:
            order.coupon = OrderCoupon(
                expiry=request.coupon.expiry,
                threshold=request.coupon.threshold,
                discount=request.coupon.discount,
            )

        return self._repo.save(order)

    def _build_cart(self, request: CheckoutRequest) -> Cart:
        items: list[CartItem] = []
        for item_in in request.items:
            product = CATALOG.get(item_in.product_name)
            if product is None:
                raise UnknownProductError(item_in.product_name)
            items.append(
                CartItem(
                    product=product,
                    qty=item_in.qty,
                    unit_price=Decimal(str(item_in.unit_price)),
                )
            )

        promotions: list[Promotion] = []
        for promo_in in request.promotions:
            category = INPUT_CATEGORY_MAP.get(promo_in.category)
            if category is None:
                category = Category[promo_in.category.upper()]
            promotions.append(
                Promotion(
                    date=promo_in.date,
                    discount_rate=Decimal(str(promo_in.discount_rate)),
                    category=category,
                )
            )

        coupon = None
        if request.coupon:
            coupon = Coupon(
                expiry=request.coupon.expiry,
                threshold=Decimal(str(request.coupon.threshold)),
                discount=Decimal(str(request.coupon.discount)),
            )

        return Cart(
            items=items,
            promotions=promotions,
            coupon=coupon,
            settlement_date=request.settled_at,
        )
