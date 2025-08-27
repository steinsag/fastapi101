import json

from confluent_kafka import Producer  # type: ignore

from app.adapter.config import kafka_config_producer
from app.domain.model.item import Item


def publish_item(item: Item) -> None:
    producer = get_kafka_producer()

    payload = {"item_id": item.id, "name": item.name, "price": item.price}
    producer.produce(
        topic="items",
        value=json.dumps(payload).encode("utf-8"),
        key=str(item.id),
    )
    producer.flush(timeout=2.0)


def get_kafka_producer() -> Producer:
    return Producer(kafka_config_producer())
