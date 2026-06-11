from api.base_client import BaseClient

class PostsAPI(BaseClient):
    def get_post(self, post_id):
        return self.get(f"/posts/{post_id}")

    def get_all_posts(self):
        return self.get("/posts")

    def get_posts_by_user(self, user_id):
        return self.session.get(f"{self.base_url}/posts", params={"userId": user_id}, timeout=10)

    def get_post_comments(self, post_id):
        return self.get(f"/posts/{post_id}/comments")

    def create_post(self, payload):
        return self.post("/posts", payload)

    def update_post(self, post_id, payload):
        return self.put(f"/posts/{post_id}", payload)

    def patch_post(self, post_id, payload):
        return self.patch(f"/posts/{post_id}", payload)

    def delete_post(self, post_id):
        return self.delete(f"/posts/{post_id}")