from unittest.mock import Mock

import pytest

from app.domain.errors import InvalidItemIdError
from app.domain.item_service import ItemService
from app.domain.model.item import Item
from tests.test.item_data import ITEM_ID, ITEM_MISSING_ID
from tests.test.item_fixture import create_item_fixture


@pytest.fixture()
def sut() -> ItemService:
    return ItemService(
        get_item_by_id_provider=lambda _item_id: None,
        create_item_provider=lambda _new_item: Item(id=ITEM_ID, name="", price=0.0),
        item_created_publisher=lambda _item: None,
    )


def test_with_valid_id_calls_provider_and_returns_item() -> None:
    item_provider = Mock(return_value=create_item_fixture())
    sut = ItemService(
        get_item_by_id_provider=item_provider,
        create_item_provider=lambda _new_item: Item(id=ITEM_ID, name="", price=0.0),
        item_created_publisher=lambda _item: None,
    )

    actual_item = sut.get_item_by_id(ITEM_ID)

    assert actual_item == create_item_fixture()
    item_provider.assert_called_once_with(ITEM_ID)


def test_with_missing_id_calls_provider_and_returns_none() -> None:
    item_provider = Mock(return_value=None)
    sut = ItemService(
        get_item_by_id_provider=item_provider,
        create_item_provider=lambda _new_item: Item(id=ITEM_ID, name="", price=0.0),
        item_created_publisher=lambda _item: None,
    )

    actual_item = sut.get_item_by_id(ITEM_MISSING_ID)

    assert actual_item is None
    item_provider.assert_called_once_with(ITEM_MISSING_ID)


def test_with_invalid_id_raises_error() -> None:
    item_provider = Mock(side_effect=InvalidItemIdError("invalid item id"))

    sut = ItemService(
        get_item_by_id_provider=item_provider,
        create_item_provider=lambda _new_item: Item(id=ITEM_ID, name="", price=0.0),
        item_created_publisher=lambda _item: None,
    )

    with pytest.raises(InvalidItemIdError):
        sut.get_item_by_id("123")
    item_provider.assert_called_once_with("123")


def test_with_no_provider_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ItemService(
            get_item_by_id_provider=None,  # type: ignore[arg-type]
            create_item_provider=lambda _new_item: Item(id=ITEM_ID, name="", price=0.0),
            item_created_publisher=lambda _item: None,
        )

    assert "get_item_by_id_provider must not be None" in str(exc_info.value)
