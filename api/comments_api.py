from api.base_client import BaseClient

class CommentsAPI(BaseClient):
    def get_comment(self, comment_id):
        return self.get(f"/comments/{comment_id}")

    def get_all_comments(self):
        return self.get("/comments")

    def get_comments_by_post(self, post_id):
        return self.session.get(f"{self.base_url}/comments", params={"postId": post_id}, timeout=10)
