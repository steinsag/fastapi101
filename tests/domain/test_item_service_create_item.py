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
    with pytest.raises(TypeError):
        ItemService()  # type: ignore[misc]


def test_with_no_id_generator_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ItemService(
            id_generator=None,  # type: ignore[arg-type]
            get_item_by_id_provider=lambda _i: None,
            create_item_provider=lambda new_item, new_id: Item(
                id=new_id, name=new_item.name, price=new_item.price
            ),
        )
    assert "id_generator must not be None" in str(exc_info.value)


def test_with_no_create_item_provider_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ItemService(
            id_generator=lambda: ITEM_ID,
            get_item_by_id_provider=lambda _i: None,
            create_item_provider=None,  # type: ignore[arg-type]
        )
    assert "create_item_provider must not be None" in str(exc_info.value)
