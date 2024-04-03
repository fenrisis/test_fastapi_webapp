from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.dependencies import get_redis
from app.main import app


def test_write_data_success():
    mock_redis = MagicMock()
    mock_redis.set.return_value = True

    app.dependency_overrides[get_redis] = lambda: mock_redis

    with TestClient(app) as client:
        response = client.post("/write_data/", json={"phone": "89090000000", "address": "123 Main St, Anytown, Country"})
        assert response.status_code == 200
        assert response.json() == {"message": "Data saved successfully"}
        mock_redis.set.assert_called_with("89090000000", "123 Main St, Anytown, Country")

    app.dependency_overrides.clear()


def test_write_data_failure_invalid_phone(client):
    response = client.post("/write_data/", json={"phone": "invalid", "address": "123 Main St, Anytown, Country"})
    assert response.status_code >= 400


def test_check_data_found(client, mock_redis):
    mock_redis.get.return_value = "123 Main St, Anytown, Country"
    response = client.get("/check_data/?phone=89090000000")
    assert response.status_code == 200
    assert response.json() == {"phone": "89090000000", "address": "123 Main St, Anytown, Country"}


def test_check_data_not_found(client, mock_redis):
    mock_redis.get.return_value = None
    response = client.get("/check_data/?phone=89090000000")
    assert response.status_code == 404
