import requests
from config.settings import BASE_URL, TIMEOUT

class BaseClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, endpoint):
        return self.session.get(f"{self.base_url}{endpoint}", timeout=TIMEOUT)

    def post(self, endpoint, payload):
        return self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT)

    def put(self, endpoint, payload):
        return self.session.put(f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT)

    def patch(self, endpoint, payload):
        return self.session.patch(f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT)

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}", timeout=TIMEOUT)