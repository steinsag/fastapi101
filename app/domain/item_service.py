from .model.item import Item


def get_item_by_id(item_id: int) -> Item | None:
    if item_id == 1:
        return Item(
            item_id=item_id,
            name="Sample Item",
            price=107.99,
        )
    else:
        return None
