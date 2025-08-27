import os
from typing import Generator

import pytest
from testcontainers.mongodb import MongoDbContainer  # type: ignore


@pytest.fixture(scope="session")
def mongodb_service() -> Generator[str, None, None]:
    with MongoDbContainer("mongo:8.0") as mongo:
        host = mongo.get_container_host_ip()
        port = mongo.get_exposed_port(27017)
        uri = f"mongodb://{host}:{port}/"

        os.environ["MONGODB_URL"] = uri

        yield uri


def test_get_connection_url(mongodb_service: str) -> None:
    assert "mongodb://localhost:" in mongodb_service
