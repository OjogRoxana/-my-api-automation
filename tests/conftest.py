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
