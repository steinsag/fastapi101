import pytest

import app.adapter.mongo_adapter as mongo_adapter
from app.adapter.mongo_adapter import get_items_collection
from tests.test.item_data import ITEM_ID
from tests.test.item_fixture import create_item_db_fixture, create_item_fixture


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = get_items_collection()
    collection.delete_many({})
    return collection


def test_get_item_by_id_returns_item_when_found(items_collection) -> None:
    items_collection.insert_one(create_item_db_fixture())

    actual = mongo_adapter.get_item_by_id(ITEM_ID)

    assert actual == create_item_fixture()


def test_get_item_by_id_returns_none_when_not_found(items_collection) -> None:
    actual = mongo_adapter.get_item_by_id(999)

    assert actual is None
