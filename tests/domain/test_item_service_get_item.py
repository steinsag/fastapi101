import pytest

from app.domain.item_service import ItemService
from app.domain.model.item import Item
from tests.test.id_generator_fixture import id_generator
from tests.test.item_data import ITEM_ID
from tests.test.item_fixture import create_item_fixture


@pytest.fixture()
def sut(id_generator) -> ItemService:
    def fake_provider(item_id: str) -> Item | None:
        if item_id == ITEM_ID:
            return create_item_fixture()
        return None

    return ItemService(
        id_generator=id_generator,
        get_item_by_id_provider=fake_provider,
        create_item_provider=lambda _new_item, new_id: Item(
            id=new_id, name="", price=0.0
        ),
    )


def test_with_valid_id_returns_item(sut: ItemService) -> None:
    actual_item = sut.get_item_by_id(ITEM_ID)

    assert actual_item == create_item_fixture()


def test_with_invalid_id_returns_none(sut: ItemService) -> None:
    actual_item = sut.get_item_by_id("123")

    assert actual_item is None


def test_with_no_provider_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ItemService(
            id_generator=lambda: ITEM_ID,
            get_item_by_id_provider=None,  # type: ignore[arg-type]
            create_item_provider=lambda _new_item, new_id: Item(
                id=new_id, name="", price=0.0
            ),
        )

    assert "get_item_by_id_provider must not be None" in str(exc_info.value)
