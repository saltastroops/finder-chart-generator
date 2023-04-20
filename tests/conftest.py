from typing import Generator

import pytest
from starlette.testclient import TestClient

from fcg.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app=app)
