from typing import Any, Callable, Iterator

import pytest
from pymongo.errors import ConfigurationError

import app.adapter.mongo_adapter as mongo_adapter


@pytest.fixture(autouse=True)
def reset_singleton() -> Iterator[None]:
    mongo_adapter._mongo_client = None  # type: ignore[attr-defined]
    yield
    mongo_adapter._mongo_client = None  # type: ignore[attr-defined]


def test_get_items_collection_raises_runtime_error_when_no_db_in_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONGODB_URL", "mongodb://user:pass@host:27017")

    class FakeClient:
        def get_default_database(self) -> Any:  # noqa: D401
            raise ConfigurationError("No default database defined")

    def fake_mongo_client(_url: str) -> FakeClient:
        return FakeClient()

    monkeypatch.setattr(mongo_adapter, "MongoClient", fake_mongo_client)  # type: ignore[arg-type]

    with pytest.raises(RuntimeError) as exc_info:
        mongo_adapter.get_items_collection()

    assert (
        str(exc_info.value)
        == "MONGODB_URL must include a database name, e.g. mongodb://user:pass@host:27017/test"
    )


def test_get_mongo_client_initialized_only_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MONGODB_URL", "mongodb://user:pass@host:27017/test")

    class FakeClient:
        pass

    call_count = {"n": 0}

    def make_client_factory(counter: dict[str, int]) -> Callable[[str], FakeClient]:
        def _factory(_url: str) -> FakeClient:
            counter["n"] += 1
            return FakeClient()

        return _factory

    factory = make_client_factory(call_count)
    monkeypatch.setattr(mongo_adapter, "MongoClient", factory)  # type: ignore[arg-type]

    c1 = mongo_adapter.get_mongo_client()
    c2 = mongo_adapter.get_mongo_client()

    assert c1 is c2
    assert call_count["n"] == 1
