from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator(".inventory_item")
        self.add_to_cart_buttons = page.locator(".btn_inventory")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def get_item_count(self):
        self.items.first.wait_for(state="visible", timeout=10000)
        return self.items.count()

    def add_first_item_to_cart(self):
        self.add_to_cart_buttons.first.wait_for(state="visible", timeout=10000)
        self.add_to_cart_buttons.first.click()

    def get_cart_count(self):
        self.cart_badge.wait_for(state="visible", timeout=10000)
        return self.cart_badge.text_content()

    def go_to_cart(self):
        self.cart_icon.wait_for(state="visible", timeout=10000)
        self.cart_icon.click()

    def logout(self):
        self.menu_button.wait_for(state="visible", timeout=10000)
        self.menu_button.click()
        self.logout_link.wait_for(state="visible", timeout=10000)
        self.logout_link.click()