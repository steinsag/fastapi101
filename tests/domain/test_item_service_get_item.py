from app.domain.item_service import ItemService
from tests.test.item_data import ITEM_ID
from tests.test.item_fixture import create_item_fixture

sut = ItemService()


def test_with_valid_id_returns_item() -> None:
    actual_item = sut.get_item_by_id(ITEM_ID)

    assert actual_item == create_item_fixture()


def test_with_invalid_id_returns_none() -> None:
    actual_item = sut.get_item_by_id(123)

    assert actual_item is None
