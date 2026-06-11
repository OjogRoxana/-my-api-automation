import pytest
from faker import Faker
import jsonschema

fake = Faker()

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
    "additionalProperties": False,
}

# ── Smoke ────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
def test_get_post_returns_200(posts_api):
    response = posts_api.get_post(1)
    assert response.status_code == 200

# ── Happy path — single post ─────────────────────────────

@pytest.mark.api
def test_get_post_has_correct_id(posts_api):
    response = posts_api.get_post(1)
    assert response.json()["id"] == 1

@pytest.mark.api
def test_get_post_has_required_fields(posts_api):
    body = posts_api.get_post(1).json()
    for field in ("id", "title", "body", "userId"):
        assert field in body

@pytest.mark.api
def test_get_post_returns_json(posts_api):
    response = posts_api.get_post(1)
    assert response.headers["Content-Type"].startswith("application/json")

@pytest.mark.api
def test_get_post_schema(posts_api):
    body = posts_api.get_post(1).json()
    jsonschema.validate(body, POST_SCHEMA)

@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_valid_post_ids_return_200(posts_api, post_id):
    assert posts_api.get_post(post_id).status_code == 200

# ── Happy path — all posts ───────────────────────────────

@pytest.mark.api
def test_get_all_posts_returns_100(posts_api):
    response = posts_api.get_all_posts()
    assert response.status_code == 200
    assert len(response.json()) == 100

@pytest.mark.api
def test_get_all_posts_schema(posts_api):
    posts = posts_api.get_all_posts().json()
    for post in posts:
        jsonschema.validate(post, POST_SCHEMA)

# ── Filtering ────────────────────────────────────────────

@pytest.mark.api
def test_get_posts_by_user_returns_200(posts_api):
    assert posts_api.get_posts_by_user(1).status_code == 200

@pytest.mark.api
def test_get_posts_by_user_only_has_that_user(posts_api):
    posts = posts_api.get_posts_by_user(1).json()
    assert len(posts) > 0
    assert all(p["userId"] == 1 for p in posts)

# ── Nested resource — comments ───────────────────────────

@pytest.mark.api
def test_get_post_comments_returns_200(posts_api):
    assert posts_api.get_post_comments(1).status_code == 200

@pytest.mark.api
def test_get_post_comments_are_non_empty(posts_api):
    comments = posts_api.get_post_comments(1).json()
    assert len(comments) > 0

@pytest.mark.api
def test_get_post_comments_belong_to_post(posts_api):
    comments = posts_api.get_post_comments(1).json()
    assert all(c["postId"] == 1 for c in comments)

# ── Create ───────────────────────────────────────────────

@pytest.mark.api
def test_create_post_returns_201(posts_api):
    payload = {"title": "Test Post", "body": "Hello", "userId": 1}
    assert posts_api.create_post(payload).status_code == 201

@pytest.mark.api
def test_create_post_returns_correct_title(posts_api):
    payload = {"title": "My Title", "body": "My Body", "userId": 1}
    assert posts_api.create_post(payload).json()["title"] == "My Title"

@pytest.mark.api
def test_create_post_with_faker_data(posts_api):
    payload = {"title": fake.sentence(), "body": fake.paragraph(), "userId": 1}
    response = posts_api.create_post(payload)
    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]

@pytest.mark.api
def test_create_post_empty_payload_responds(posts_api):
    response = posts_api.create_post({})
    assert response.status_code in (200, 201)

# ── Update (PUT) ─────────────────────────────────────────

@pytest.mark.api
def test_update_post_returns_200(posts_api):
    payload = {"id": 1, "title": "Updated", "body": "Updated body", "userId": 1}
    assert posts_api.update_post(1, payload).status_code == 200

@pytest.mark.api
def test_update_post_reflects_new_title(posts_api):
    new_title = fake.sentence()
    payload = {"id": 1, "title": new_title, "body": "body", "userId": 1}
    body = posts_api.update_post(1, payload).json()
    assert body["title"] == new_title

# ── Patch ────────────────────────────────────────────────

@pytest.mark.api
def test_patch_post_returns_200(posts_api):
    assert posts_api.patch_post(1, {"title": "Patched"}).status_code == 200

@pytest.mark.api
def test_patch_post_only_changes_patched_field(posts_api):
    new_title = fake.sentence()
    body = posts_api.patch_post(1, {"title": new_title}).json()
    assert body["title"] == new_title
    assert "userId" in body

# ── Delete ───────────────────────────────────────────────

@pytest.mark.api
def test_delete_post_returns_200(posts_api):
    assert posts_api.delete_post(1).status_code == 200

@pytest.mark.api
def test_delete_post_returns_empty_body(posts_api):
    body = posts_api.delete_post(1).json()
    assert body == {}

# ── Negative / edge ──────────────────────────────────────

@pytest.mark.api
def test_get_nonexistent_post_returns_404(posts_api):
    assert posts_api.get_post(99999).status_code == 404

@pytest.mark.api
def test_get_post_id_zero_returns_404(posts_api):
    assert posts_api.get_post(0).status_code == 404

# ── Performance ──────────────────────────────────────────

@pytest.mark.api
def test_response_time_is_acceptable(posts_api):
    import time
    start = time.time()
    posts_api.get_post(1)
    assert time.time() - start < 3.0
