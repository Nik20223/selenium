import random

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


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
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "#content .product-miniature .price")

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

    def product_prices(self) -> list[str]:
        return [element.text for element in self.find_all(self.PRODUCT_PRICES)]

    def open_random_product(self) -> str:
        """Open a random product from the home page and return its name."""
        card = random.choice(self.find_all(self.PRODUCTS))
        title = card.find_element(*self.PRODUCT_TITLE)
        name = title.text
        title.click()
        return name
