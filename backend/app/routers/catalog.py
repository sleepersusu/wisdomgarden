from fastapi import APIRouter

from app.schemas.order import SuccessResponse
from shopping_cart.domain.product import CATALOG, INPUT_NAME_MAP

router = APIRouter(prefix="/catalog", tags=["catalog"])

# Reverse map: catalog key -> Chinese display name
_KEY_TO_DISPLAY: dict[str, str] = {v: k for k, v in INPUT_NAME_MAP.items()}


@router.get("", response_model=SuccessResponse[list[dict]])
def list_catalog():
    data = [
        {
            "key": key,
            "display_name": _KEY_TO_DISPLAY.get(key, key),
            "category": product.category.value,
        }
        for key, product in CATALOG.items()
    ]
    return SuccessResponse(data=data)
