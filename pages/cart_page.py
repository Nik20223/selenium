from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/cart"

    ITEM_NAMES = (By.CSS_SELECTOR, ".cart-items .product-line-info a.label")

    def product_names(self) -> list[str]:
        return [element.text for element in self.find_all(self.ITEM_NAMES)]
