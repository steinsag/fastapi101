import os
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

from app.domain.errors import InvalidItemIdError
from app.domain.model.item import Item
from app.domain.model.new_item import NewItem

_mongo_client: MongoClient | None = None

MONGODB_ITEMS_COLLECTION = "items"


def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        mongodb_url = os.environ["MONGODB_URL"]
        _mongo_client = MongoClient(mongodb_url)
    return _mongo_client


def get_items_collection() -> Any:
    mongodb_url = os.environ.get("MONGODB_URL")
    if not mongodb_url:
        raise RuntimeError("MONGODB_URL environment variable is required")
    client = get_mongo_client()
    try:
        db = client.get_default_database()
    except ConfigurationError as exc:
        raise RuntimeError(
            "MONGODB_URL must include a database name, e.g. mongodb://user:pass@host:27017/test"
        ) from exc
    return db[MONGODB_ITEMS_COLLECTION]


def get_item_by_id(item_id: str) -> Item | None:
    try:
        object_id = ObjectId(item_id)
    except InvalidId:
        raise InvalidItemIdError("item_id must be a valid ObjectId") from None

    collection = get_items_collection()
    doc = collection.find_one({"_id": object_id}, {"_id": 1, "name": 1, "price": 1})
    if doc is None:
        return None
    return Item(id=str(doc["_id"]), name=str(doc["name"]), price=float(doc["price"]))


def create_item(new_item: NewItem) -> Item:
    collection = get_items_collection()
    doc = {"name": new_item.name, "price": new_item.price}
    result = collection.insert_one(doc)
    return Item(id=str(result.inserted_id), name=new_item.name, price=new_item.price)
