import os
from typing import Any, Dict, Iterable, Optional

from pymongo import MongoClient
from pymongo.errors import ConfigurationError

from app.domain.model.item import Item

_mongo_client: MongoClient | None = None

MONGODB_ITEMS_COLLECTION = "items"


class InMemoryCollection:
    def __init__(self) -> None:
        self._docs: Dict[int, Dict[str, Any]] = {}

    def delete_many(self, _filter: Dict[str, Any]) -> Any:
        self._docs.clear()

        class _Result:
            deleted_count = 0

        return _Result()

    def insert_one(self, doc: Dict[str, Any]) -> Any:
        _id = int(doc["_id"])  # tests guarantee _id exists
        self._docs[_id] = {k: v for k, v in doc.items()}

        class _Result:
            inserted_id = _id

        return _Result()

    def find_one(
        self, _filter: Dict[str, Any], projection: Optional[Dict[str, int]] = None
    ) -> Optional[Dict[str, Any]]:
        _id = _filter.get("_id")
        if _id is None:
            return None
        key = int(_id)
        doc = self._docs.get(key)
        if doc is None:
            return None
        if projection is None:
            return {k: v for k, v in doc.items()}
        include_keys: Iterable[str] = (k for k, v in projection.items() if v)
        return {k: doc[k] for k in include_keys if k in doc}


_in_memory_collection = InMemoryCollection()


def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        mongodb_url = os.environ["MONGODB_URL"]
        _mongo_client = MongoClient(mongodb_url)
    return _mongo_client


def get_items_collection() -> Any:
    mongodb_url = os.environ.get("MONGODB_URL")
    if not mongodb_url:
        return _in_memory_collection
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
