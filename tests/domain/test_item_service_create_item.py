import pytest

from app.domain.item_service import ItemService
from app.domain.model.item import Item
from app.domain.model.new_item import NewItem
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE


@pytest.fixture()
def sut() -> ItemService:
    def id_gen() -> int:
        return ITEM_ID

    def create_provider(new_item: NewItem, new_id: int) -> Item:
        assert new_id == ITEM_ID
        return Item(id=new_id, name=new_item.name, price=new_item.price)

    return ItemService(
        id_generator=id_gen,
        get_item_by_id_provider=lambda _i: None,
        create_item_provider=create_provider,
    )


def test_create_item_returns_created_item(sut: ItemService) -> None:
    new_item = NewItem(name=ITEM_NAME, price=ITEM_PRICE)

    created = sut.create_item(new_item)

    assert created.id == ITEM_ID
    assert created.name == ITEM_NAME
    assert created.price == ITEM_PRICE


def test_create_item_without_configuration_raises() -> None:
    service = ItemService()

    with pytest.raises(RuntimeError) as exc_info:
        service.create_item(NewItem(name=ITEM_NAME, price=ITEM_PRICE))

    assert "Create item is not configured" in str(exc_info.value)
