import pytest
from typing import Callable


@pytest.fixture()
def id_generator() -> Callable[[], int]:
    return lambda: 1
