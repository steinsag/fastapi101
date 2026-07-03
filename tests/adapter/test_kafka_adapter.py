import json

import pytest
from confluent_kafka import KafkaException

import app.adapter.kafka_adapter as kafka_adapter
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
        assert actual_msg.key() == create_item_fixture().id.encode("utf-8")
        val = actual_msg.value()
        assert val is not None
        data = json.loads(val.decode("utf-8"))
        actual_item = Item(id=data["item_id"], name=data["name"], price=data["price"])
        assert actual_item == create_item_fixture()


def test_publish_item_propagates_produce_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingProducer:
        def produce(self, **_kwargs) -> None:
            raise KafkaException("publish failed")

        def flush(self, timeout: float) -> None:
            raise AssertionError("flush should not be called")

    monkeypatch.setattr(
        kafka_adapter,
        "get_kafka_producer",
        lambda: FailingProducer(),
    )

    with pytest.raises(KafkaException, match="publish failed"):
        publish_item(create_item_fixture())
