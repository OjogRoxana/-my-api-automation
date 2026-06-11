import pytest
import jsonschema

TODO_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "completed"],
    "properties": {
        "userId":    {"type": "integer"},
        "id":        {"type": "integer"},
        "title":     {"type": "string"},
        "completed": {"type": "boolean"},
    },
    "additionalProperties": False,
}

# ── Smoke ────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
def test_get_todo_returns_200(todos_api):
    assert todos_api.get_todo(1).status_code == 200

# ── Happy path — single todo ─────────────────────────────

@pytest.mark.api
def test_get_todo_has_correct_id(todos_api):
    assert todos_api.get_todo(1).json()["id"] == 1

@pytest.mark.api
def test_get_todo_completed_is_boolean(todos_api):
    assert isinstance(todos_api.get_todo(1).json()["completed"], bool)

@pytest.mark.api
def test_get_todo_schema(todos_api):
    jsonschema.validate(todos_api.get_todo(1).json(), TODO_SCHEMA)

@pytest.mark.api
@pytest.mark.parametrize("todo_id", [1, 100, 200])
def test_valid_todo_ids_return_200(todos_api, todo_id):
    assert todos_api.get_todo(todo_id).status_code == 200

# ── Happy path — all todos ───────────────────────────────

@pytest.mark.api
def test_get_all_todos_returns_200(todos_api):
    assert todos_api.get_all_todos().status_code == 200

@pytest.mark.api
def test_get_all_todos_returns_200_items(todos_api):
    assert len(todos_api.get_all_todos().json()) == 200

@pytest.mark.api
def test_get_all_todos_schema(todos_api):
    for todo in todos_api.get_all_todos().json():
        jsonschema.validate(todo, TODO_SCHEMA)

# ── Filtering ────────────────────────────────────────────

@pytest.mark.api
def test_get_completed_todos_returns_200(todos_api):
    assert todos_api.get_todos_by_completed(True).status_code == 200

@pytest.mark.api
def test_get_completed_todos_are_all_completed(todos_api):
    todos = todos_api.get_todos_by_completed(True).json()
    assert len(todos) > 0
    assert all(t["completed"] is True for t in todos)

@pytest.mark.api
def test_get_incomplete_todos_are_all_incomplete(todos_api):
    todos = todos_api.get_todos_by_completed(False).json()
    assert len(todos) > 0
    assert all(t["completed"] is False for t in todos)

@pytest.mark.api
def test_completed_and_incomplete_sum_to_total(todos_api):
    total = len(todos_api.get_all_todos().json())
    done = len(todos_api.get_todos_by_completed(True).json())
    not_done = len(todos_api.get_todos_by_completed(False).json())
    assert done + not_done == total

# ── Negative ─────────────────────────────────────────────

@pytest.mark.api
def test_get_nonexistent_todo_returns_404(todos_api):
    assert todos_api.get_todo(99999).status_code == 404

@pytest.mark.api
def test_get_todo_id_zero_returns_404(todos_api):
    assert todos_api.get_todo(0).status_code == 404
