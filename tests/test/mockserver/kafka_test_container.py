import os
from typing import Generator

import pytest
from confluent_kafka.admin import AdminClient, NewTopic  # type: ignore
from testcontainers.kafka import KafkaContainer  # type: ignore


@pytest.fixture(scope="session")
def kafka_service() -> Generator[str, None, None]:
    with KafkaContainer() as kafka:
        os.environ["KAFKA_ENDPOINT"] = kafka.get_bootstrap_server()
        os.environ["KAFKA_USERNAME"] = "testuser"
        os.environ["KAFKA_PASSWORD"] = "testpass"
        os.environ["KAFKA_SECURITY_PROTOCOL"] = "PLAINTEXT"

        admin_client = AdminClient(
            conf={"bootstrap.servers": kafka.get_bootstrap_server()}
        )
        topic = NewTopic("items", num_partitions=1, replication_factor=1)
        admin_client.create_topics([topic])

        yield kafka.get_bootstrap_server()
