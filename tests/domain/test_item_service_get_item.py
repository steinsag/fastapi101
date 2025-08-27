import os

import pytest

from app.adapter.mongo_adapter import get_items_collection
from app.domain.item_service import ItemService
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE
from tests.test.item_fixture import create_item_fixture
from tests.test.mockserver.mongodb_test_container import mongodb_service


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = get_items_collection()
    collection.delete_many({})
    return collection


@pytest.fixture()
def sut(items_collection) -> ItemService:
    return ItemService(items_collection_provider=lambda: items_collection)


def test_with_valid_id_returns_item(sut: ItemService, items_collection) -> None:
    items_collection.insert_one({"id": ITEM_ID, "name": ITEM_NAME, "price": ITEM_PRICE})

    actual_item = sut.get_item_by_id(ITEM_ID)

    assert actual_item == create_item_fixture()


def test_with_invalid_id_returns_none(sut: ItemService, items_collection) -> None:
    actual_item = sut.get_item_by_id(123)

    assert actual_item is None


def test_with_no_provider_raises_error() -> None:
    sut = ItemService(items_collection_provider=None)

    with pytest.raises(RuntimeError) as exc_info:
        sut.get_item_by_id(ITEM_ID)

    assert "Items collection provider is not configured" in str(exc_info.value)
