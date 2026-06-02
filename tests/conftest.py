import pytest
from api.posts_api import PostsAPI

@pytest.fixture
def posts_api():
    return PostsAPI()