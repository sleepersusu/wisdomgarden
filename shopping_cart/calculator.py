from decimal import ROUND_HALF_UP, Decimal

from shopping_cart.cart import Cart


class CartCalculator:
    @staticmethod
    def calculate(cart: Cart) -> Decimal:
        total = Decimal("0")

        for item in cart.items:
            subtotal = Decimal(str(item.qty)) * item.unit_price

            for promo in cart.promotions:
                if promo.date == cart.settlement_date and promo.category == item.product.category:
                    subtotal *= promo.discount_rate
                    break

            total += subtotal

        if (
            cart.coupon is not None
            and cart.settlement_date <= cart.coupon.expiry
            and total >= cart.coupon.threshold
        ):
            total -= cart.coupon.discount

        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
