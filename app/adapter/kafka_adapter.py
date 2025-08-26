import json
from dataclasses import asdict

from confluent_kafka import Producer  # type: ignore

from app.adapter.config import kafka_config_producer
from app.domain.model.item import Item


def publish_item(item: Item) -> None:
    producer = get_kafka_producer()

    producer.produce(
        topic="items",
        value=json.dumps(asdict(item)).encode("utf-8"),
        key=str(item.item_id),
    )
    producer.flush(timeout=2.0)


def get_kafka_producer() -> Producer:
    return Producer(kafka_config_producer())
