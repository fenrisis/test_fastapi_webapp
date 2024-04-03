import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.dependencies import get_redis
from app.main import app


@pytest.fixture(scope="module")
def client(mock_redis):
    app.dependency_overrides[get_redis] = lambda: mock_redis
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
def mock_redis():
    mock = MagicMock()
    mock.get.return_value = None
    return mock
