from types import TracebackType

from confluent_kafka import Consumer


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
            }  # type: ignore[arg-type]
        )

    def __enter__(self) -> Consumer:
        self.consumer.subscribe([self.topic])
        return self.consumer

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        self.consumer.close()
        return None
