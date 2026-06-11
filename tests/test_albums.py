import pytest
import jsonschema

ALBUM_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title"],
    "properties": {
        "userId": {"type": "integer"},
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
    },
    "additionalProperties": False,
}

PHOTO_SCHEMA = {
    "type": "object",
    "required": ["albumId", "id", "title", "url", "thumbnailUrl"],
    "properties": {
        "albumId":      {"type": "integer"},
        "id":           {"type": "integer"},
        "title":        {"type": "string"},
        "url":          {"type": "string"},
        "thumbnailUrl": {"type": "string"},
    },
    "additionalProperties": False,
}

# ── Smoke ────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
def test_get_album_returns_200(albums_api):
    assert albums_api.get_album(1).status_code == 200

# ── Happy path — single album ────────────────────────────

@pytest.mark.api
def test_get_album_has_correct_id(albums_api):
    assert albums_api.get_album(1).json()["id"] == 1

@pytest.mark.api
def test_get_album_schema(albums_api):
    jsonschema.validate(albums_api.get_album(1).json(), ALBUM_SCHEMA)

# ── Happy path — all albums ──────────────────────────────

@pytest.mark.api
def test_get_all_albums_returns_200(albums_api):
    assert albums_api.get_all_albums().status_code == 200

@pytest.mark.api
def test_get_all_albums_returns_100(albums_api):
    assert len(albums_api.get_all_albums().json()) == 100

@pytest.mark.api
def test_get_all_albums_schema(albums_api):
    for album in albums_api.get_all_albums().json():
        jsonschema.validate(album, ALBUM_SCHEMA)

# ── Nested resource — photos ─────────────────────────────

@pytest.mark.api
def test_get_album_photos_returns_200(albums_api):
    assert albums_api.get_album_photos(1).status_code == 200

@pytest.mark.api
def test_get_album_photos_are_non_empty(albums_api):
    assert len(albums_api.get_album_photos(1).json()) > 0

@pytest.mark.api
def test_get_album_photos_belong_to_album(albums_api):
    photos = albums_api.get_album_photos(1).json()
    assert all(p["albumId"] == 1 for p in photos)

@pytest.mark.api
def test_get_album_photos_schema(albums_api):
    for photo in albums_api.get_album_photos(1).json():
        jsonschema.validate(photo, PHOTO_SCHEMA)

# ── Negative ─────────────────────────────────────────────

@pytest.mark.api
def test_get_nonexistent_album_returns_404(albums_api):
    assert albums_api.get_album(99999).status_code == 404
