import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def client():
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.mark.anyio
async def test_catalog_returns_all_products(client):
    response = await client.get("/api/catalog")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 18


@pytest.mark.anyio
async def test_catalog_items_have_required_fields(client):
    response = await client.get("/api/catalog")
    first = response.json()["data"][0]
    assert "key" in first
    assert "display_name" in first
    assert "category" in first
