import os
from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConfigurationError

_mongo_client: MongoClient | None = None

MONGODB_ITEMS_COLLECTION = "items"


def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        mongodb_url = os.environ["MONGODB_URL"]
        _mongo_client = MongoClient(mongodb_url)
    return _mongo_client


def get_items_collection() -> Any:
    client = get_mongo_client()
    try:
        db = client.get_default_database()
    except ConfigurationError as exc:
        raise RuntimeError(
            "MONGODB_URL must include a database name, e.g. mongodb://user:pass@host:27017/test"
        ) from exc
    return db[MONGODB_ITEMS_COLLECTION]
