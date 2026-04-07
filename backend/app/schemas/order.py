from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_key: str
    qty: int
    unit_price: float


class OrderPromotionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    promo_date: date
    discount_rate: float
    category: str


class OrderCouponResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    expiry: date
    threshold: float
    discount: float


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    settled_at: date
    total_amount: float
    created_at: datetime


class OrderDetailResponse(OrderResponse):
    items: list[OrderItemResponse] = []
    promotions: list[OrderPromotionResponse] = []
    coupon: OrderCouponResponse | None = None


class PaginationMeta(BaseModel):
    page: int
    size: int
    total_elements: int
    total_pages: int


class PaginatedOrdersData(BaseModel):
    items: list[OrderResponse]
    pagination: PaginationMeta


class SuccessResponse[T](BaseModel):
    success: bool = True
    data: T
