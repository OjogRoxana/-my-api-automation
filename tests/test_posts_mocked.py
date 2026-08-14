import pytest
from unittest.mock import patch, MagicMock
from api.posts_api import PostsAPI

# ── Mock a successful response ───────────────────────────

@pytest.mark.api
def test_get_post_uses_correct_endpoint():
    with patch("api.base_client.requests.Session") as mock_session:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "title": "Mocked title",
            "body": "Mocked body",
            "userId": 1
        }
        mock_session.return_value.get.return_value = mock_response

        api = PostsAPI()
        response = api.get_post(1)

        assert response.status_code == 200
        assert response.json()["title"] == "Mocked title"

# ── Mock a 500 server error ──────────────────────────────

@pytest.mark.api
def test_api_handles_server_error():
    with patch("api.base_client.requests.Session") as mock_session:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_session.return_value.get.return_value = mock_response

        api = PostsAPI()
        response = api.get_post(1)

        assert response.status_code == 500

# ── Mock a timeout ───────────────────────────────────────

@pytest.mark.api
def test_api_handles_timeout():
    import requests as req
    with patch("api.base_client.requests.Session") as mock_session:
        mock_session.return_value.get.side_effect = req.exceptions.Timeout

        api = PostsAPI()

        with pytest.raises(req.exceptions.Timeout):
            api.get_post(1)

# ── Mock a connection error ──────────────────────────────

@pytest.mark.api
def test_api_handles_connection_error():
    import requests as req
    with patch("api.base_client.requests.Session") as mock_session:
        mock_session.return_value.get.side_effect = req.exceptions.ConnectionError

        api = PostsAPI()

        with pytest.raises(req.exceptions.ConnectionError):
            api.get_post(1)

# ── Mock using pytest fixture for reuse ──────────────────

@pytest.fixture
def mock_posts_api():
    with patch("api.base_client.requests.Session") as mock_session:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "title": "Test", "body": "Body", "userId": 1}
        mock_session.return_value.get.return_value = mock_response
        yield PostsAPI()

@pytest.mark.api
def test_mocked_api_fixture(mock_posts_api):
    response = mock_posts_api.get_post(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1