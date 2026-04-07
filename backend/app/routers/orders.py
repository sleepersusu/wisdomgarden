import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.exceptions import OrderNotFoundError
from app.repositories.order_repository import OrderRepository
from app.schemas.order import (
    OrderDetailResponse,
    OrderResponse,
    PaginatedOrdersData,
    PaginationMeta,
    SuccessResponse,
)

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_repository(session: Session = Depends(get_session)) -> OrderRepository:
    return OrderRepository(session)


@router.get("", response_model=SuccessResponse[PaginatedOrdersData])
def list_orders(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    repo: OrderRepository = Depends(get_order_repository),
):
    items, total = repo.list_paginated(page, size)
    return SuccessResponse(
        data=PaginatedOrdersData(
            items=[OrderResponse.model_validate(o) for o in items],
            pagination=PaginationMeta(
                page=page,
                size=size,
                total_elements=total,
                total_pages=max(1, math.ceil(total / size)),
            ),
        )
    )


@router.get("/{order_id}", response_model=SuccessResponse[OrderDetailResponse])
def get_order(
    order_id: int,
    repo: OrderRepository = Depends(get_order_repository),
):
    order = repo.find_by_id(order_id)
    if order is None:
        raise OrderNotFoundError(order_id)
    return SuccessResponse(data=OrderDetailResponse.model_validate(order))
