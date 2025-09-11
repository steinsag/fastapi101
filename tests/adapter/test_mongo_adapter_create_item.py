import pytest

import app.adapter.mongo_adapter as mongo_adapter
from app.domain.model.item import Item
from app.domain.model.new_item import NewItem
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = mongo_adapter.get_items_collection()
    collection.delete_many({})
    return collection


def test_create_item_inserts_and_returns_item(items_collection) -> None:
    new_item = NewItem(name=ITEM_NAME, price=ITEM_PRICE)

    created = mongo_adapter.create_item(new_item=new_item, new_id=ITEM_ID)

    assert isinstance(created, Item)
    assert created.id == ITEM_ID
    assert created.name == ITEM_NAME
    assert created.price == ITEM_PRICE

    stored = items_collection.find_one({"_id": ITEM_ID})
    assert stored == {"_id": ITEM_ID, "name": ITEM_NAME, "price": ITEM_PRICE}


def test_generate_new_id_returns_int() -> None:
    new_id = mongo_adapter.generate_new_id()

    assert isinstance(new_id, int)
    assert new_id > 0
