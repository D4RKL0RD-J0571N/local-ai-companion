import pytest
from unittest.mock import patch, MagicMock

import requests
from core.lmstudio_client import LMStudioClient


@pytest.fixture
def client():
    return LMStudioClient(base_url="http://mocked-api")


def test_send_message_success(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "Hello human!"}}
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = client.send_message([{"role": "user", "content": "Hi"}])

        assert result == "Hello human!"
        mock_post.assert_called_once()
        payload = mock_post.call_args.kwargs["json"]
        assert payload["messages"][0]["content"] == "Hi"


def test_send_message_failure_returns_none(client):
    with patch("requests.post", side_effect=requests.RequestException("Connection error")):
        result = client.send_message([{"role": "user", "content": "Hi"}])
        assert result is None


def test_send_message_invalid_json(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"invalid": "schema"}
    mock_response.raise_for_status = MagicMock()

    with patch("requests.post", return_value=mock_response):
        result = client.send_message([{"role": "user", "content": "Hi"}])
        assert result is None
