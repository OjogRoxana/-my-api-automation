from playwright.sync_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator(".inventory_item")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def get_item_count(self):
        return self.items.count()

    def add_first_item_to_cart(self):
        self.page.locator(".btn_inventory").first.click()

    def get_cart_count(self):
        return self.cart_badge.text_content()

    def go_to_cart(self):
        self.cart_icon.click()