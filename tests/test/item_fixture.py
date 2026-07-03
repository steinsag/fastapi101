from app.domain.model.item import Item
from app.rest.dto.item_dto import ItemDto
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE


def create_item_fixture() -> Item:
    return Item(
        id=ITEM_ID,
        name=ITEM_NAME,
        price=ITEM_PRICE,
    )


def create_item_dto_fixture() -> ItemDto:
    return ItemDto(
        id=ITEM_ID,
        name=ITEM_NAME,
        price=ITEM_PRICE,
    )


def create_item_db_fixture(item_id) -> dict:
    return {
        "_id": item_id,
        "name": ITEM_NAME,
        "price": ITEM_PRICE,
    }
