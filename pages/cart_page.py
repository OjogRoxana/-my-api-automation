from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.remove_button = page.locator(".cart_item button.btn_secondary")

    def get_cart_item_count(self):
        self.page.wait_for_load_state("networkidle", timeout=10000)
        return self.cart_items.count()

    def proceed_to_checkout(self):
        self.checkout_button.wait_for(state="visible", timeout=10000)
        self.checkout_button.click()

    def remove_item(self):
        self.remove_button.first.wait_for(state="visible", timeout=10000)
        self.remove_button.first.click()