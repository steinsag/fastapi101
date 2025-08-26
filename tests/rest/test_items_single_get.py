import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_with_valid_item_returns_success() -> None:
    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"item_id": 1, "q": None}


def test_with_query_string_returns_success() -> None:
    response = client.get("/items/1?q=test")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"item_id": 1, "q": "test"}


def test_with_string_item_id_returns_422() -> None:
    response = client.get("/items/abc")

    assert response.status_code == 422


@pytest.mark.parametrize(
    "given_accept_header",
    [
        "application/xml",
        "text/plain",
    ],
)
def test_with_requesting_plain_text_returns_406(given_accept_header: str) -> None:
    response = client.get("/items/1", headers={"Accept": given_accept_header})

    assert response.status_code == 406
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"detail": "Not Acceptable"}
