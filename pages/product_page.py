import allure
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
    INFORMATION = (By.CSS_SELECTOR, ".product-information")
    DESCRIPTION = (By.CSS_SELECTOR, "#description")

    KEY_ELEMENTS = {
        "title": TITLE,
        "cover image": COVER_IMAGE,
        "price": PRICE,
        "quantity input": QUANTITY_INPUT,
        "add to cart button": ADD_TO_CART,
        "product information": INFORMATION,
        "description": DESCRIPTION,
    }

    def name(self) -> str:
        """Full product name as shown on the product page."""
        return self.get_text(self.TITLE).strip()

    def can_be_added_to_cart(self) -> bool:
        """True when the product adds to the cart without choosing extra options."""
        return self.find(self.ADD_TO_CART).is_enabled()

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self) -> "ProductPage":
        self.click(self.ADD_TO_CART)
        self.find(self.ADD_TO_CART_CONFIRMATION)
        self.logger.info("Товар добавлен в корзину")
        return self
