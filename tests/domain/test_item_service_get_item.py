import pytest

from app.domain.item_service import ItemService
from app.domain.model.item import Item
from tests.test.item_data import ITEM_ID
from tests.test.item_fixture import create_item_fixture


@pytest.fixture()
def sut() -> ItemService:
    def fake_provider(item_id: int) -> Item | None:
        if item_id == ITEM_ID:
            return create_item_fixture()
        return None

    return ItemService(get_item_by_id_provider=fake_provider)


def test_with_valid_id_returns_item(sut: ItemService) -> None:
    actual_item = sut.get_item_by_id(ITEM_ID)

    assert actual_item == create_item_fixture()


def test_with_invalid_id_returns_none(sut: ItemService) -> None:
    actual_item = sut.get_item_by_id(123)

    assert actual_item is None


def test_with_no_provider_raises_error() -> None:
    sut = ItemService(get_item_by_id_provider=None)

    with pytest.raises(RuntimeError) as exc_info:
        sut.get_item_by_id(ITEM_ID)

    assert "Item provider is not configured" in str(exc_info.value)
