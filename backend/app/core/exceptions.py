from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code


class OrderNotFoundError(AppError):
    def __init__(self, order_id: int) -> None:
        super().__init__("ORDER_NOT_FOUND", f"Order {order_id} not found", status_code=404)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"code": exc.code, "message": exc.message, "details": []},
        },
    )
