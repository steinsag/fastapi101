from confluent_kafka import Consumer  # type: ignore


class KafkaTestConsumer:
    topic: str
    consumer: Consumer

    def __init__(self, kafka_service: str, topic: str) -> None:
        self.topic = topic
        self.consumer = Consumer({
            'bootstrap.servers': kafka_service,
            'group.id': 'test_group',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'default.topic.config': {'auto.offset.reset': 'earliest'}
        })

    def __enter__(self) -> Consumer:
        self.consumer.subscribe([self.topic])
        return self.consumer

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        self.consumer.close()
