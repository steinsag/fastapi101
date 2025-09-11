import pytest
from fastapi.testclient import TestClient

from app.domain.item_service import ItemService
from app.domain.item_service_protocol import ItemServiceProtocol
from app.domain.model.item import Item
from app.main import app
from tests.test.item_fixture import create_item_dto_fixture, create_item_fixture

client = TestClient(app)


def test_with_valid_item_returns_success() -> None:
    app.dependency_overrides[ItemService] = (
        lambda: __create_fake_item_service_with_response(create_item_fixture())
    )

    try:
        response = client.get("/items/1")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == create_item_dto_fixture().__dict__
    finally:
        app.dependency_overrides.pop(ItemService, None)


def test_with_unknown_item_id_returns_404() -> None:
    app.dependency_overrides[ItemService] = (
        lambda: __create_fake_item_service_with_response(None)
    )

    try:
        response = client.get("/items/123")

        assert response.status_code == 404
        assert response.json() == {}
    finally:
        app.dependency_overrides.pop(ItemService, None)


@pytest.mark.parametrize(
    "given_accept_header",
    [
        "application/xml",
        "text/plain",
    ],
)
def test_with_requesting_plain_text_returns_406(given_accept_header: str) -> None:
    app.dependency_overrides[ItemService] = (
        lambda: __create_fake_item_service_failing_on_any_call()
    )

    try:
        response = client.get("/items/1", headers={"Accept": given_accept_header})
        assert response.status_code == 406
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == {"detail": "Not Acceptable"}
    finally:
        app.dependency_overrides.pop(ItemService, None)


def test_with_internal_error_returns_500_and_hides_details() -> None:
    class FailingService(ItemServiceProtocol):
        def get_item_by_id(self, item_id: str):
            raise RuntimeError("boom: internal failure")

    app.dependency_overrides[ItemService] = lambda: FailingService()

    try:
        response = client.get("/items/999")
        assert response.status_code == 500
        assert response.headers["Content-Type"] == "application/json"
        body = response.json()
        assert body == {"detail": "Internal Server Error"}
        assert "boom" not in str(body)
    finally:
        app.dependency_overrides.pop(ItemService, None)


def __create_fake_item_service_with_response(
    given_response_item: Item | None,
) -> ItemServiceProtocol:
    class FakeItemService(ItemServiceProtocol):
        def get_item_by_id(self, item_id: str):
            return given_response_item

    return FakeItemService()


def __create_fake_item_service_failing_on_any_call() -> ItemServiceProtocol:
    class FakeItemService(ItemServiceProtocol):
        def get_item_by_id(self, item_id: str):
            raise AssertionError("ItemService should not be called")

    return FakeItemService()
