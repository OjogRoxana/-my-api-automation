import pytest

USER_SCHEMA_REQUIRED = ["id", "name", "username", "email", "address", "phone", "website", "company"]
ADDRESS_FIELDS = ["street", "city", "zipcode"]
COMPANY_FIELDS = ["name", "catchPhrase", "bs"]

# ── Smoke ────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
def test_get_user_returns_200(users_api):
    assert users_api.get_user(1).status_code == 200

# ── Happy path — single user ─────────────────────────────

@pytest.mark.api
def test_get_user_has_email(users_api):
    body = users_api.get_user(1).json()
    assert "email" in body
    assert "@" in body["email"]

@pytest.mark.api
def test_get_user_has_all_required_fields(users_api):
    body = users_api.get_user(1).json()
    for field in USER_SCHEMA_REQUIRED:
        assert field in body, f"Missing field: {field}"

@pytest.mark.api
def test_get_user_id_is_integer(users_api):
    body = users_api.get_user(1).json()
    assert isinstance(body["id"], int)

@pytest.mark.api
def test_get_user_name_is_string(users_api):
    body = users_api.get_user(1).json()
    assert isinstance(body["name"], str) and len(body["name"]) > 0

@pytest.mark.api
def test_get_user_address_has_required_subfields(users_api):
    address = users_api.get_user(1).json()["address"]
    for field in ADDRESS_FIELDS:
        assert field in address, f"Missing address field: {field}"

@pytest.mark.api
def test_get_user_company_has_required_subfields(users_api):
    company = users_api.get_user(1).json()["company"]
    for field in COMPANY_FIELDS:
        assert field in company, f"Missing company field: {field}"

@pytest.mark.api
def test_get_user_correct_id_in_response(users_api):
    assert users_api.get_user(5).json()["id"] == 5

# ── Happy path — all users ───────────────────────────────

@pytest.mark.api
def test_get_all_users_returns_list(users_api):
    response = users_api.get_all_users()
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.api
def test_get_all_users_returns_exactly_10(users_api):
    assert len(users_api.get_all_users().json()) == 10

@pytest.mark.api
def test_get_all_users_each_has_email(users_api):
    users = users_api.get_all_users().json()
    assert all("email" in u and "@" in u["email"] for u in users)

# ── Boundary ─────────────────────────────────────────────

@pytest.mark.api
def test_get_last_valid_user_returns_200(users_api):
    assert users_api.get_user(10).status_code == 200

@pytest.mark.api
def test_get_user_just_outside_range_returns_404(users_api):
    assert users_api.get_user(11).status_code == 404

# ── Negative ─────────────────────────────────────────────

@pytest.mark.api
def test_get_nonexistent_user_returns_404(users_api):
    assert users_api.get_user(99999).status_code == 404

# ── Nested resources ─────────────────────────────────────

@pytest.mark.api
def test_get_user_posts_returns_200(users_api):
    assert users_api.get_user_posts(1).status_code == 200

@pytest.mark.api
def test_get_user_posts_are_non_empty(users_api):
    posts = users_api.get_user_posts(1).json()
    assert len(posts) > 0

@pytest.mark.api
def test_get_user_posts_belong_to_user(users_api):
    posts = users_api.get_user_posts(1).json()
    assert all(p["userId"] == 1 for p in posts)

@pytest.mark.api
def test_get_user_todos_returns_200(users_api):
    assert users_api.get_user_todos(1).status_code == 200

@pytest.mark.api
def test_get_user_todos_are_non_empty(users_api):
    assert len(users_api.get_user_todos(1).json()) > 0

@pytest.mark.api
def test_get_user_albums_returns_200(users_api):
    assert users_api.get_user_albums(1).status_code == 200

@pytest.mark.api
def test_get_user_albums_are_non_empty(users_api):
    assert len(users_api.get_user_albums(1).json()) > 0

# ── Performance ──────────────────────────────────────────

@pytest.mark.api
def test_get_all_users_response_time(users_api):
    import time
    start = time.time()
    users_api.get_all_users()
    assert time.time() - start < 3.0
