import pytest
from fastapi.testclient import TestClient

from app.adapter.mongo_adapter import get_items_collection
from app.main import app
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE
from tests.test.item_fixture import create_item_dto_fixture, create_item_db_fixture
from tests.test.mockserver.mongodb_test_container import mongodb_service

client = TestClient(app)


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = get_items_collection()
    collection.delete_many({})
    return collection


def test_get_item_existing_returns_item(items_collection) -> None:
    items_collection.insert_one(create_item_db_fixture())

    response = client.get(f"/items/{ITEM_ID}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == create_item_dto_fixture().__dict__


def test_get_item_missing_returns_404(items_collection) -> None:
    response = client.get("/items/123")

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {}
