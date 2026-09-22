from locust import HttpUser, task, between


class JSONPlaceholderUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://jsonplaceholder.typicode.com"

    @task(3)
    def get_post(self):
        self.client.get("/posts/1", name="/posts/{id}")

    @task(2)
    def get_all_posts(self):
        self.client.get("/posts", name="/posts")

    @task(1)
    def create_post(self):
        payload = {
            "title": "Performance test post",
            "body": "Testing under load",
            "userId": 1
        }
        self.client.post("/posts", json=payload, name="/posts [POST]")

    @task(2)
    def get_user(self):
        self.client.get("/users/1", name="/users/{id}")

    @task(1)
    def get_comments(self):
        self.client.get("/posts/1/comments", name="/posts/{id}/comments")