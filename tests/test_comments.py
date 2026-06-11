import pytest
import jsonschema

COMMENT_SCHEMA = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {"type": "integer"},
        "id":     {"type": "integer"},
        "name":   {"type": "string"},
        "email":  {"type": "string"},
        "body":   {"type": "string"},
    },
    "additionalProperties": False,
}

# ── Smoke ────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
def test_get_comment_returns_200(comments_api):
    assert comments_api.get_comment(1).status_code == 200

# ── Happy path — single comment ──────────────────────────

@pytest.mark.api
def test_get_comment_has_correct_id(comments_api):
    assert comments_api.get_comment(1).json()["id"] == 1

@pytest.mark.api
def test_get_comment_has_email(comments_api):
    body = comments_api.get_comment(1).json()
    assert "email" in body and "@" in body["email"]

@pytest.mark.api
def test_get_comment_schema(comments_api):
    jsonschema.validate(comments_api.get_comment(1).json(), COMMENT_SCHEMA)

# ── Happy path — all comments ────────────────────────────

@pytest.mark.api
def test_get_all_comments_returns_200(comments_api):
    assert comments_api.get_all_comments().status_code == 200

@pytest.mark.api
def test_get_all_comments_returns_500(comments_api):
    assert len(comments_api.get_all_comments().json()) == 500

@pytest.mark.api
def test_get_all_comments_schema(comments_api):
    for comment in comments_api.get_all_comments().json():
        jsonschema.validate(comment, COMMENT_SCHEMA)

# ── Filtering ────────────────────────────────────────────

@pytest.mark.api
def test_get_comments_by_post_returns_200(comments_api):
    assert comments_api.get_comments_by_post(1).status_code == 200

@pytest.mark.api
def test_get_comments_by_post_are_non_empty(comments_api):
    assert len(comments_api.get_comments_by_post(1).json()) > 0

@pytest.mark.api
def test_get_comments_by_post_belong_to_post(comments_api):
    comments = comments_api.get_comments_by_post(1).json()
    assert all(c["postId"] == 1 for c in comments)

@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 5, 10])
def test_filter_comments_by_various_post_ids(comments_api, post_id):
    comments = comments_api.get_comments_by_post(post_id).json()
    assert all(c["postId"] == post_id for c in comments)

# ── Negative ─────────────────────────────────────────────

@pytest.mark.api
def test_get_nonexistent_comment_returns_404(comments_api):
    assert comments_api.get_comment(99999).status_code == 404
