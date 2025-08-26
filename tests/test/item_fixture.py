from app.domain.model.item import Item
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE


def create_item_fixture() -> Item:
    return Item(
        item_id=ITEM_ID,
        name=ITEM_NAME,
        price=ITEM_PRICE,
    )
