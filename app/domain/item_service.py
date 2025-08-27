from .item_service_protocol import ItemServiceProtocol
from .model.item import Item


class ItemService(ItemServiceProtocol):
    def get_item_by_id(self, item_id: int) -> Item | None:
        if item_id == 1:
            return Item(
                id=item_id,
                name="Sample Item",
                price=107.99,
            )
        else:
            return None
