import pytest
from api.posts_api import PostsAPI
from api.users_api import UsersAPI
from api.comments_api import CommentsAPI
from api.todos_api import TodosAPI
from api.albums_api import AlbumsAPI

@pytest.fixture
def posts_api():
    return PostsAPI()

@pytest.fixture
def users_api():
    return UsersAPI()

@pytest.fixture
def comments_api():
    return CommentsAPI()

@pytest.fixture
def todos_api():
    return TodosAPI()

@pytest.fixture
def albums_api():
    return AlbumsAPI()

# Reusable valid post IDs for parametrize
VALID_POST_IDS = [1, 10, 50, 100]
INVALID_POST_IDS = [0, -1, 99999]

def pytest_configure(config):
    config.addinivalue_line("markers", "parametrize: parametrized test cases")