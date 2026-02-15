from collections.abc import Callable

from .item_service_protocol import ItemServiceProtocol
from .model.item import Item
from .model.new_item import NewItem


class ItemService(ItemServiceProtocol):
    def __init__(
        self,
        id_generator: Callable[[], str],
        get_item_by_id_provider: Callable[[str], Item | None],
        create_item_provider: Callable[[NewItem, str], Item],
    ):
        if id_generator is None:
            raise ValueError("id_generator must not be None")
        if get_item_by_id_provider is None:
            raise ValueError("get_item_by_id_provider must not be None")
        if create_item_provider is None:
            raise ValueError("create_item_provider must not be None")
        self._id_generator = id_generator
        self._get_item_by_id_provider = get_item_by_id_provider
        self._create_item_provider = create_item_provider

    def get_item_by_id(self, item_id: str) -> Item | None:
        return self._get_item_by_id_provider(item_id)

    def create_item(self, new_item: NewItem) -> Item:
        new_id = self._id_generator()
        return self._create_item_provider(new_item, new_id)
