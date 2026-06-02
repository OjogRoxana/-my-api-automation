from api.base_client import BaseClient

class PostsAPI(BaseClient):
    def get_post(self, post_id):
        return self.get(f"/posts/{post_id}")

    def get_all_posts(self):
        return self.get("/posts")

    def create_post(self, payload):
        return self.post("/posts", payload)