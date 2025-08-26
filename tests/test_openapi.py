import pytest
from fastapi.testclient import TestClient

from app.main import app

OPENAPI_URLS = ["/docs", "/redoc", "/openapi.json"]


@pytest.mark.parametrize("given_url", OPENAPI_URLS)
def test_openapi_spec_disabled_by_default(
    given_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = TestClient(app)

    actual = client.get(given_url)

    assert actual.status_code == 404
