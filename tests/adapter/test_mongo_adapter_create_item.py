import pytest
from bson import ObjectId
from pymongo.errors import PyMongoError

import app.adapter.mongo_adapter as mongo_adapter
from app.domain.model.item import Item
from app.domain.model.new_item import NewItem
from tests.test.item_data import ITEM_NAME, ITEM_PRICE


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = mongo_adapter.get_items_collection()
    collection.delete_many({})
    return collection


def test_create_item_inserts_and_returns_item(items_collection) -> None:
    new_item = NewItem(name=ITEM_NAME, price=ITEM_PRICE)

    created = mongo_adapter.create_item(new_item=new_item)

    assert isinstance(created, Item)
    assert ObjectId.is_valid(created.id)
    assert created.name == ITEM_NAME
    assert created.price == ITEM_PRICE

    stored = items_collection.find_one({"_id": ObjectId(created.id)})
    assert stored == {
        "_id": ObjectId(created.id),
        "name": ITEM_NAME,
        "price": ITEM_PRICE,
    }


def test_create_item_propagates_insert_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingCollection:
        def insert_one(self, doc: dict) -> None:
            raise PyMongoError("insert failed")

    monkeypatch.setattr(
        mongo_adapter,
        "get_items_collection",
        lambda: FailingCollection(),
    )

    with pytest.raises(PyMongoError, match="insert failed"):
        mongo_adapter.create_item(NewItem(name=ITEM_NAME, price=ITEM_PRICE))
