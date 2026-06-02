import pytest

@pytest.mark.api
def test_get_post_returns_200(posts_api):
    response = posts_api.get_post(1)
    assert response.status_code == 200

@pytest.mark.api
def test_get_post_has_correct_id(posts_api):
    response = posts_api.get_post(1)
    assert response.json()["id"] == 1

@pytest.mark.api
def test_create_post_returns_201(posts_api):
    payload = {"title": "Test Post", "body": "Hello", "userId": 1}
    response = posts_api.create_post(payload)
    assert response.status_code == 201