import logging
from collections.abc import Callable

from .item_service_protocol import ItemServiceProtocol
from .model.item import Item
from .model.new_item import NewItem

logger = logging.getLogger(__name__)


class ItemService(ItemServiceProtocol):
    def __init__(
        self,
        get_item_by_id_provider: Callable[[str], Item | None],
        create_item_provider: Callable[[NewItem], Item],
        item_created_publisher: Callable[[Item], None],
    ):
        if get_item_by_id_provider is None:
            raise ValueError("get_item_by_id_provider must not be None")
        if create_item_provider is None:
            raise ValueError("create_item_provider must not be None")
        if item_created_publisher is None:
            raise ValueError("item_created_publisher must not be None")
        self._get_item_by_id_provider = get_item_by_id_provider
        self._create_item_provider = create_item_provider
        self._item_created_publisher = item_created_publisher

    def get_item_by_id(self, item_id: str) -> Item | None:
        return self._get_item_by_id_provider(item_id)

    def create_item(self, new_item: NewItem) -> Item:
        created_item = self._create_item_provider(new_item)
        try:
            self._item_created_publisher(created_item)
        except Exception:
            logger.exception("Failed to publish item-created event")
        return created_item
