import pytest
from bson import ObjectId

import app.adapter.mongo_adapter as mongo_adapter
from app.adapter.mongo_adapter import get_items_collection
from app.domain.errors import InvalidItemIdError
from tests.test.item_data import ITEM_ID
from tests.test.item_fixture import create_item_db_fixture, create_item_fixture


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = get_items_collection()
    collection.delete_many({})
    return collection


def test_get_item_by_id_returns_item_when_found(items_collection) -> None:
    items_collection.insert_one(create_item_db_fixture(ObjectId(ITEM_ID)))

    actual = mongo_adapter.get_item_by_id(ITEM_ID)

    assert actual == create_item_fixture()


def test_get_item_by_id_returns_none_when_not_found(items_collection) -> None:
    actual = mongo_adapter.get_item_by_id("507f1f77bcf86cd799439012")

    assert actual is None


def test_get_item_by_id_raises_for_invalid_object_id(items_collection) -> None:
    with pytest.raises(InvalidItemIdError):
        mongo_adapter.get_item_by_id("123")
