from collections.abc import Callable

import pytest

from tests.test.item_data import ITEM_ID


@pytest.fixture()
def id_generator() -> Callable[[], str]:
    return lambda: ITEM_ID
