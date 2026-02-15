import os
from collections.abc import Generator
from urllib.parse import urlparse

import pytest
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture(scope="session")
def mongodb_service() -> Generator[str]:
    with MongoDbContainer("mongo:8.0") as mongo:
        uri = mongo.get_connection_url()
        parsed = urlparse(uri)
        hostport = parsed.netloc.split("@")[-1]
        if parsed.username and parsed.password:
            uri = f"mongodb://{parsed.username}:{parsed.password}@{hostport}/test?authSource=admin"
        else:
            uri = f"mongodb://{hostport}/test"

        os.environ["MONGODB_URL"] = uri

        yield uri


def test_get_connection_url(mongodb_service: str) -> None:
    assert "mongodb://localhost:" in mongodb_service
