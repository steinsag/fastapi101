import os
from typing import Any

from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

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


def get_item_by_id(item_id: int) -> Item | None:
    collection = get_items_collection()
    doc = collection.find_one({"_id": item_id}, {"_id": 1, "name": 1, "price": 1})
    if doc is None:
        return None
    return Item(id=int(doc["_id"]), name=str(doc["name"]), price=float(doc["price"]))


def generate_new_id() -> int:
    oid = ObjectId()
    return int(str(oid), 16)


def create_item(new_item: NewItem, new_id: int) -> Item:
    collection = get_items_collection()
    doc = {"_id": int(new_id), "name": new_item.name, "price": float(new_item.price)}
    collection.insert_one(doc)
    return Item(id=int(new_id), name=new_item.name, price=float(new_item.price))
