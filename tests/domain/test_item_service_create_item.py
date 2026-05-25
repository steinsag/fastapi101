from unittest.mock import Mock

import pytest

from app.domain.item_service import ItemService
from app.domain.model.item import Item
from app.domain.model.new_item import NewItem
from tests.test.item_data import ITEM_ID, ITEM_NAME, ITEM_PRICE


@pytest.fixture()
def sut() -> ItemService:
    return ItemService(
        get_item_by_id_provider=lambda _i: None,
        create_item_provider=lambda new_item: Item(
            id=ITEM_ID, name=new_item.name, price=new_item.price
        ),
        item_created_publisher=lambda _item: None,
    )


def test_create_item_returns_persisted_item(sut: ItemService) -> None:
    new_item = NewItem(name=ITEM_NAME, price=ITEM_PRICE)

    created = sut.create_item(new_item)

    assert created.id == ITEM_ID
    assert created.name == ITEM_NAME
    assert created.price == ITEM_PRICE


def test_create_item_calls_persistence_and_publisher_adapters() -> None:
    new_item = NewItem(name=ITEM_NAME, price=ITEM_PRICE)
    persisted_item = Item(id=ITEM_ID, name=ITEM_NAME, price=ITEM_PRICE)
    mongodb_create_adapter = Mock(return_value=persisted_item)
    kafka_publish_adapter = Mock()

    sut = ItemService(
        get_item_by_id_provider=lambda _i: None,
        create_item_provider=mongodb_create_adapter,
        item_created_publisher=kafka_publish_adapter,
    )

    created_item = sut.create_item(new_item)

    assert created_item == persisted_item
    mongodb_create_adapter.assert_called_once_with(new_item)
    kafka_publish_adapter.assert_called_once_with(persisted_item)


def test_create_item_without_configuration_raises() -> None:
    with pytest.raises(TypeError):
        ItemService()  # type: ignore[misc]


def test_create_item_does_not_publish_when_persistence_fails() -> None:
    published_items: list[Item] = []

    def failing_provider(_new_item: NewItem) -> Item:
        raise RuntimeError("mongo failed")

    sut = ItemService(
        get_item_by_id_provider=lambda _i: None,
        create_item_provider=failing_provider,
        item_created_publisher=published_items.append,
    )

    with pytest.raises(RuntimeError, match="mongo failed"):
        sut.create_item(NewItem(name=ITEM_NAME, price=ITEM_PRICE))

    assert published_items == []


def test_create_item_logs_and_returns_created_item_when_publish_fails(
    caplog: pytest.LogCaptureFixture,
) -> None:
    expected_item = Item(id=ITEM_ID, name=ITEM_NAME, price=ITEM_PRICE)

    def failing_publisher(_item: Item) -> None:
        raise RuntimeError("kafka failed")

    sut = ItemService(
        get_item_by_id_provider=lambda _i: None,
        create_item_provider=lambda _item: expected_item,
        item_created_publisher=failing_publisher,
    )

    created = sut.create_item(NewItem(name=ITEM_NAME, price=ITEM_PRICE))

    assert created == expected_item
    assert "Failed to publish item-created event" in caplog.text
    assert "kafka failed" in caplog.text


def test_with_no_create_item_provider_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ItemService(
            get_item_by_id_provider=lambda _i: None,
            create_item_provider=None,  # type: ignore[arg-type]
            item_created_publisher=lambda _item: None,
        )
    assert "create_item_provider must not be None" in str(exc_info.value)


def test_with_no_item_created_publisher_raises_error() -> None:
    with pytest.raises(ValueError) as exc_info:
        ItemService(
            get_item_by_id_provider=lambda _i: None,
            create_item_provider=lambda new_item: Item(
                id=ITEM_ID, name=new_item.name, price=new_item.price
            ),
            item_created_publisher=None,  # type: ignore[arg-type]
        )
    assert "item_created_publisher must not be None" in str(exc_info.value)
