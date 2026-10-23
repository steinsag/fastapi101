import json
import time

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.adapter.mongo_adapter import get_items_collection
from app.main import app
from tests.test.item_data import ITEM_NAME, ITEM_PRICE
from tests.test.mockserver.kafka_test_consumer import KafkaTestConsumer
from tests.test.mockserver.kafka_test_container import kafka_service
from tests.test.mockserver.mongodb_test_container import mongodb_service

client = TestClient(app)
POLL_TIMEOUT = 10.0


@pytest.fixture()
def items_collection(mongodb_service: str):
    collection = get_items_collection()
    collection.delete_many({})
    return collection


def test_create_item_persists_item_and_publishes_event(
    items_collection,
    kafka_service: str,
) -> None:
    with KafkaTestConsumer(kafka_service, "items") as consumer:
        response = client.post(
            "/items",
            json={"name": ITEM_NAME, "price": ITEM_PRICE},
            headers={"Accept": "application/json"},
        )

        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/json"
        body = response.json()
        assert ObjectId.is_valid(body["id"])
        assert body["name"] == ITEM_NAME
        assert body["price"] == ITEM_PRICE

        stored = items_collection.find_one({"_id": ObjectId(body["id"])})
        assert stored == {
            "_id": ObjectId(body["id"]),
            "name": ITEM_NAME,
            "price": ITEM_PRICE,
        }

        event = __poll_item_event(consumer, body["id"])
        assert event == {
            "item_id": body["id"],
            "name": ITEM_NAME,
            "price": ITEM_PRICE,
        }


def __poll_item_event(consumer, item_id: str) -> dict[str, str | float]:
    deadline = time.monotonic() + POLL_TIMEOUT
    while time.monotonic() < deadline:
        msg = consumer.poll(timeout=0.5)
        if msg is None:
            continue
        val = msg.value()
        if val is None:
            continue
        data = json.loads(val.decode("utf-8"))
        if data.get("item_id") == item_id:
            return data
    raise AssertionError(f"No Kafka event found for item {item_id}")
