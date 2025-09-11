from typing import Any, Callable

from .item_service_protocol import ItemServiceProtocol
from .model.item import Item


class ItemService(ItemServiceProtocol):
    def __init__(self, items_collection_provider: Callable[[], Any] | None = None):
        self._items_collection_provider = items_collection_provider

    def get_item_by_id(self, item_id: int) -> Item | None:
        provider = self._items_collection_provider
        if provider is None:
            raise RuntimeError("Items collection provider is not configured")

        collection = provider()
        doc = collection.find_one({"_id": item_id}, {"_id": 1, "name": 1, "price": 1})
        if doc is None:
            return None
        return Item(
            id=int(doc["_id"]), name=str(doc["name"]), price=float(doc["price"])
        )
