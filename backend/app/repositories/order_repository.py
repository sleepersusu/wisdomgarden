from sqlalchemy.orm import Session

from app.models.order import Order, OrderCoupon, OrderItem, OrderPromotion


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> Order:
        self._session.add(order)
        self._session.flush()
        self._session.refresh(order)
        return order

    def find_by_id(self, order_id: int) -> Order | None:
        return self._session.get(Order, order_id)

    def list_paginated(self, page: int, size: int) -> tuple[list[Order], int]:
        total = self._session.query(Order).count()
        items = (
            self._session.query(Order)
            .order_by(Order.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        return items, total
