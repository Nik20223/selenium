import random

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.product_page import ProductPage


class MainPage(BasePage):
    PATH = "/"

    LOGO = (By.CSS_SELECTOR, "#_desktop_logo .logo")
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search_widget input[name='s']")
    CART = (By.CSS_SELECTOR, ".blockcart")
    USER_INFO = (By.CSS_SELECTOR, ".user-info")
    CURRENCY_SELECTOR = (By.CSS_SELECTOR, "#_desktop_currency_selector")
    TOP_MENU = (By.CSS_SELECTOR, "#_desktop_top_menu")
    CONTACT_LINK = (By.CSS_SELECTOR, "#_desktop_contact_link")
    FOOTER = (By.CSS_SELECTOR, "#footer")

    PRODUCTS = (By.CSS_SELECTOR, "#content .product-miniature")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "#content .product-miniature .price")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title a")

    ACCOUNT = (By.CSS_SELECTOR, ".user-info a.account")

    KEY_ELEMENTS = {
        "logo": LOGO,
        "search input": SEARCH_INPUT,
        "cart block": CART,
        "user info block": USER_INFO,
        "currency selector": CURRENCY_SELECTOR,
        "top menu": TOP_MENU,
        "contact link": CONTACT_LINK,
        "footer": FOOTER,
    }

    def account_name(self) -> str:
        """Name of the signed-in customer shown in the header."""
        return self.get_text(self.ACCOUNT).strip()

    def open_random_product(self) -> ProductPage:
        """Open a random product that can be added to the cart directly."""
        total = len(self.find_all(self.PRODUCTS))
        for index in random.sample(range(total), total):
            card = self.find_all(self.PRODUCTS)[index]
            card.find_element(*self.PRODUCT_TITLE).click()
            page = ProductPage(self.driver, self.base_url)
            if page.can_be_added_to_cart():
                return page
            self.open()
        raise AssertionError("На главной нет товара, который можно добавить в корзину")
