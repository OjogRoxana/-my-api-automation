import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.fixture
def logged_in_page(page):
    login = LoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("https://www.saucedemo.com/inventory.html")
    return page

@pytest.mark.ui
def test_inventory_shows_six_items(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    assert inventory.get_item_count() == 6

@pytest.mark.ui
def test_add_item_updates_cart_badge(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_first_item_to_cart()
    assert inventory.get_cart_count() == "1"

@pytest.mark.ui
def test_cart_contains_added_item(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()
    cart = CartPage(logged_in_page)
    assert cart.get_cart_item_count() == 1

@pytest.mark.ui
def test_remove_item_empties_cart(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()
    cart = CartPage(logged_in_page)
    cart.remove_item()
    assert cart.get_cart_item_count() == 0

@pytest.mark.ui
def test_full_checkout_flow_completes_order(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    cart = CartPage(logged_in_page)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.fill_checkout_info("Roxana", "Ojog", "400000")
    checkout.finish_order()

    assert "Thank you for your order" in checkout.get_confirmation_message()