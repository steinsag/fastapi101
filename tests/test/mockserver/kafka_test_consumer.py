from confluent_kafka import Consumer  # type: ignore
from types import TracebackType
from typing import Optional


class KafkaTestConsumer:
    topic: str
    consumer: Consumer

    def __init__(self, kafka_service: str, topic: str) -> None:
        self.topic = topic
        self.consumer = Consumer(
            {
                "bootstrap.servers": kafka_service,
                "group.id": "test_group",
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False,
                "default.topic.config": {"auto.offset.reset": "earliest"},
            }
        )

    def __enter__(self) -> Consumer:
        self.consumer.subscribe([self.topic])
        return self.consumer

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        self.consumer.close()
        return None
