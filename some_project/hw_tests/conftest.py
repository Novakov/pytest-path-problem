from typing import Any

import pytest


@pytest.fixture()
def value_from_argument(request: Any) -> str:
    return request.config.getoption('--argument')
