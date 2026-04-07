from datetime import date

from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    product_name: str
    qty: int = Field(..., ge=1)
    unit_price: float = Field(..., gt=0)


class PromotionIn(BaseModel):
    date: date
    discount_rate: float = Field(..., gt=0, le=1)
    category: str


class CouponIn(BaseModel):
    expiry: date
    threshold: float = Field(..., gt=0)
    discount: float = Field(..., gt=0)


class CheckoutRequest(BaseModel):
    settled_at: date
    items: list[ItemIn] = Field(..., min_length=1)
    promotions: list[PromotionIn] = []
    coupon: CouponIn | None = None
