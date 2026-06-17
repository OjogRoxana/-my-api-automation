from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.remove_button = page.locator("[data-test='remove-sauce-labs-backpack']")

    def get_cart_item_count(self):
        return self.cart_items.count()

    def proceed_to_checkout(self):
        self.checkout_button.click()

    def remove_item(self):
        self.remove_button.click()