from typing import Callable

from .item_service_protocol import ItemServiceProtocol
from .model.item import Item


class ItemService(ItemServiceProtocol):
    def __init__(
        self, get_item_by_id_provider: Callable[[int], Item | None] | None = None
    ):
        self._get_item_by_id_provider = get_item_by_id_provider

    def get_item_by_id(self, item_id: int) -> Item | None:
        provider = self._get_item_by_id_provider
        if provider is None:
            raise RuntimeError("Item provider is not configured")

        return provider(item_id)
