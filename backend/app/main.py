from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_tables
from app.core.exceptions import AppError, app_error_handler
from app.routers import catalog, checkout, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="WisdomGarden Cart API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)

app.include_router(catalog.router, prefix="/api")
app.include_router(checkout.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
