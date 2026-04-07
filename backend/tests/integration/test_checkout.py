import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_session
import app.models.order  # noqa: F401 — registers ORM models with Base.metadata


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


VALID_PAYLOAD = {
    "settled_at": "2015-11-11",
    "items": [
        {"product_name": "ipad", "qty": 1, "unit_price": 2399.00},
        {"product_name": "monitor", "qty": 1, "unit_price": 1799.00},
        {"product_name": "beer", "qty": 12, "unit_price": 25.00},
        {"product_name": "bread", "qty": 5, "unit_price": 9.00},
    ],
    "promotions": [{"date": "2015-11-11", "discount_rate": 0.7, "category": "電子"}],
    "coupon": {"expiry": "2016-03-02", "threshold": 1000, "discount": 200},
}


@pytest.mark.anyio
async def test_checkout_returns_201_with_total(client):
    response = await client.post("/api/checkouts", json=VALID_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert abs(body["data"]["total_amount"] - 3083.60) < 0.01


@pytest.mark.anyio
async def test_checkout_without_coupon_succeeds(client):
    payload = {**VALID_PAYLOAD, "coupon": None}
    response = await client.post("/api/checkouts", json=payload)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_checkout_unknown_product_returns_422(client):
    payload = {
        "settled_at": "2015-11-11",
        "items": [{"product_name": "nonexistent", "qty": 1, "unit_price": 100}],
    }
    response = await client.post("/api/checkouts", json=payload)
    assert response.status_code == 422
