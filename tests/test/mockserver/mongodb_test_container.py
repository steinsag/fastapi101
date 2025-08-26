import os
from typing import Generator

import pytest
from testcontainers.mongodb import MongoDbContainer  # type: ignore


@pytest.fixture(scope="session")
def mongodb_service() -> Generator[str, None, None]:
    with MongoDbContainer() as mongo:
        os.environ["MONGODB_URI"] = "test"
        os.environ["MONGO_URI"] = "test"
        os.environ["MONGO_URL"] = "test"

        yield mongo.get_connection_url()
