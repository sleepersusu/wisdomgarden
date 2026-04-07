from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.exceptions import AppError
from app.schemas.checkout import CheckoutRequest
from app.schemas.order import OrderDetailResponse, SuccessResponse
from app.services.checkout_service import CheckoutService
from shopping_cart.parser import UnknownProductError

router = APIRouter(prefix="/checkouts", tags=["checkouts"])


def get_checkout_service(session: Session = Depends(get_session)) -> CheckoutService:
    return CheckoutService(session)


@router.post(
    "",
    response_model=SuccessResponse[OrderDetailResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_checkout(
    body: CheckoutRequest,
    service: CheckoutService = Depends(get_checkout_service),
):
    try:
        order = service.checkout(body)
    except UnknownProductError as exc:
        raise AppError(
            code="VALIDATION_FAILED",
            message=str(exc),
            status_code=422,
        ) from exc

    return SuccessResponse(data=OrderDetailResponse.model_validate(order))
