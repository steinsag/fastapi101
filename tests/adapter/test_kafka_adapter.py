import json

from confluent_kafka import Consumer  # type: ignore

from app.adapter.kafka_adapter import publish_item
from app.domain.model.item import Item
from tests.test.item_fixture import create_item_fixture
from tests.test.mockserver.kafka_test_consumer import KafkaTestConsumer
from tests.test.mockserver.kafka_test_container import kafka_service

POLL_TIMEOUT = 10.0


def test_publish_item(kafka_service: str) -> None:
    with KafkaTestConsumer(kafka_service, "items") as consumer:
        publish_item(create_item_fixture())

        actual_msg = consumer.poll(timeout=POLL_TIMEOUT)

        assert actual_msg is not None
        data = json.loads(actual_msg.value().decode("utf-8"))
        actual_item = Item(
            item_id=data["item_id"], name=data["name"], price=data["price"]
        )
        assert actual_item == create_item_fixture()
