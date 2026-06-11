import pytest
from pages.login_page import LoginPage

@pytest.mark.ui
def test_valid_login(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("https://www.saucedemo.com/inventory.html")
    assert page.url == "https://www.saucedemo.com/inventory.html"

@pytest.mark.ui
def test_invalid_login_shows_error(page):
    login = LoginPage(page)
    login.navigate()
    login.login("wrong_user", "wrong_pass")
    assert ("Username and password do not match" in login.get_error_message())