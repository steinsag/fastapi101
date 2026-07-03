import pytest
from fastapi.testclient import TestClient

from app.domain.item_service import ItemService
from app.domain.item_service_protocol import ItemServiceProtocol
from app.domain.model.item import Item
from app.domain.model.new_item import NewItem
from app.main import app, item_service_provider
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE
from tests.test.item_fixture import create_item_fixture

client = TestClient(app)


def test_create_item_returns_created_item() -> None:
    fake_service = RecordingCreateItemService(create_item_fixture())
    app.dependency_overrides[ItemService] = lambda: fake_service

    try:
        response = client.post(
            "/items",
            json={"name": ITEM_NAME, "price": ITEM_PRICE},
            headers={"Accept": "application/json"},
        )

        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {
            "id": ITEM_ID,
            "name": ITEM_NAME,
            "price": ITEM_PRICE,
        }
        assert fake_service.created_items == [NewItem(name=ITEM_NAME, price=ITEM_PRICE)]
    finally:
        app.dependency_overrides[ItemService] = item_service_provider


@pytest.mark.parametrize(
    "given_accept_header",
    [
        "application/xml",
        "text/plain",
    ],
)
def test_create_item_with_requesting_plain_text_returns_406(
    given_accept_header: str,
) -> None:
    app.dependency_overrides[ItemService] = (
        lambda: __create_fake_item_service_failing_on_any_call()
    )

    try:
        response = client.post(
            "/items",
            json={"name": ITEM_NAME, "price": ITEM_PRICE},
            headers={"Accept": given_accept_header},
        )
        assert response.status_code == 406
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {"detail": "Not Acceptable"}
    finally:
        app.dependency_overrides[ItemService] = item_service_provider


def test_create_item_with_internal_error_returns_500_and_hides_details() -> None:
    class FailingService(ItemServiceProtocol):
        def get_item_by_id(self, item_id: str) -> Item | None:
            raise AssertionError("ItemService should not be called")

        def create_item(self, new_item: NewItem) -> Item:
            raise RuntimeError("boom: internal failure")

    app.dependency_overrides[ItemService] = lambda: FailingService()

    try:
        response = client.post(
            "/items",
            json={"name": ITEM_NAME, "price": ITEM_PRICE},
            headers={"Accept": "application/json"},
        )
        assert response.status_code == 500
        assert response.headers["Content-Type"] == "application/json"
        body = response.json()
        assert body == {"detail": "Internal Server Error"}
        assert "boom" not in str(body)
    finally:
        app.dependency_overrides[ItemService] = item_service_provider


def test_create_item_with_malformed_body_returns_validation_error() -> None:
    app.dependency_overrides[ItemService] = (
        lambda: __create_fake_item_service_failing_on_any_call()
    )

    try:
        response = client.post(
            "/items",
            json={"name": ITEM_NAME},
            headers={"Accept": "application/json"},
        )

        assert response.status_code == 422
        assert response.headers["Content-Type"] == "application/json"
    finally:
        app.dependency_overrides[ItemService] = item_service_provider


class RecordingCreateItemService(ItemServiceProtocol):
    def __init__(self, response_item: Item) -> None:
        self.response_item = response_item
        self.created_items: list[NewItem] = []

    def get_item_by_id(self, item_id: str) -> Item | None:
        raise AssertionError("ItemService should not be called")

    def create_item(self, new_item: NewItem) -> Item:
        self.created_items.append(new_item)
        return self.response_item


def __create_fake_item_service_failing_on_any_call() -> ItemServiceProtocol:
    class FakeItemService(ItemServiceProtocol):
        def get_item_by_id(self, item_id: str) -> Item | None:
            raise AssertionError("ItemService should not be called")

        def create_item(self, new_item: NewItem) -> Item:
            raise AssertionError("ItemService should not be called")

    return FakeItemService()
