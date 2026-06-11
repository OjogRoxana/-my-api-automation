from api.base_client import BaseClient

class TodosAPI(BaseClient):
    def get_todo(self, todo_id):
        return self.get(f"/todos/{todo_id}")

    def get_all_todos(self):
        return self.get("/todos")

    def get_todos_by_completed(self, completed: bool):
        value = "true" if completed else "false"
        return self.session.get(f"{self.base_url}/todos", params={"completed": value}, timeout=10)
