from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):
    PATH = "/"

    TITLE = (By.CSS_SELECTOR, "#main h1")
    COVER_IMAGE = (By.CSS_SELECTOR, ".product-cover img")
    PRICE = (By.CSS_SELECTOR, ".product-prices .current-price")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "#quantity_wanted")
    ADD_TO_CART = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    ADD_TO_CART_CONFIRMATION = (By.CSS_SELECTOR, "#blockcart-modal")
    AVAILABILITY = (By.CSS_SELECTOR, "#product-availability")
    INFORMATION = (By.CSS_SELECTOR, ".product-information")
    DESCRIPTION = (By.CSS_SELECTOR, "#description")

    KEY_ELEMENTS = {
        "title": TITLE,
        "cover image": COVER_IMAGE,
        "price": PRICE,
        "quantity input": QUANTITY_INPUT,
        "add to cart button": ADD_TO_CART,
        "availability": AVAILABILITY,
        "product information": INFORMATION,
        "description": DESCRIPTION,
    }

    def add_to_cart(self) -> "ProductPage":
        self.click(self.ADD_TO_CART)
        self.find(self.ADD_TO_CART_CONFIRMATION)
        return self
