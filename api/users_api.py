from api.base_client import BaseClient

class UsersAPI(BaseClient):
    def get_user(self, user_id):
        return self.get(f"/users/{user_id}")

    def get_all_users(self):
        return self.get("/users")

    def get_user_posts(self, user_id):
        return self.get(f"/users/{user_id}/posts")

    def get_user_todos(self, user_id):
        return self.get(f"/users/{user_id}/todos")

    def get_user_albums(self, user_id):
        return self.get(f"/users/{user_id}/albums")
