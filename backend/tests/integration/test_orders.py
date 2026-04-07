import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_session
import app.models.order  # noqa: F401


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
async def client(test_engine):
    TestSession = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

    def override_get_session():
        session = TestSession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    from app.main import app
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


CHECKOUT_PAYLOAD = {
    "settled_at": "2015-11-11",
    "items": [{"product_name": "ipad", "qty": 1, "unit_price": 2399.00}],
    "promotions": [],
    "coupon": None,
}


@pytest.mark.anyio
async def test_list_orders_returns_paginated_response(client):
    await client.post("/api/checkouts", json=CHECKOUT_PAYLOAD)
    response = await client.get("/api/orders")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "items" in body["data"]
    assert "pagination" in body["data"]
    assert body["data"]["pagination"]["total_elements"] == 1


@pytest.mark.anyio
async def test_get_order_detail_returns_items(client):
    checkout = await client.post("/api/checkouts", json=CHECKOUT_PAYLOAD)
    order_id = checkout.json()["data"]["id"]
    response = await client.get(f"/api/orders/{order_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == order_id
    assert len(body["data"]["items"]) == 1


@pytest.mark.anyio
async def test_get_order_not_found_returns_404(client):
    response = await client.get("/api/orders/99999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "ORDER_NOT_FOUND"
