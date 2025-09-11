from typing import Callable

from .item_service_protocol import ItemServiceProtocol
from .model.item import Item
from .model.new_item import NewItem


class ItemService(ItemServiceProtocol):
    def __init__(
        self,
        id_generator: Callable[[], int] | None = None,
        get_item_by_id_provider: Callable[[int], Item | None] | None = None,
        create_item_provider: Callable[[NewItem, int], Item] | None = None,
    ):
        self._id_generator = id_generator
        self._get_item_by_id_provider = get_item_by_id_provider
        self._create_item_provider = create_item_provider

    def get_item_by_id(self, item_id: int) -> Item | None:
        provider = self._get_item_by_id_provider
        if provider is None:
            raise RuntimeError("Item provider is not configured")

        return provider(item_id)

    def create_item(self, new_item: NewItem) -> Item:
        id_generator = self._id_generator
        create_provider = self._create_item_provider
        if id_generator is None or create_provider is None:
            raise RuntimeError("Create item is not configured")
        new_id = id_generator()
        return create_provider(new_item, new_id)
