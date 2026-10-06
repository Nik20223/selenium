from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.product_page import ProductPage


class CatalogPage(BasePage):
    PATH = "/9-art"

    CATEGORY_BLOCK = (By.CSS_SELECTOR, "#main .block-category")
    PAGE_TITLE = (By.CSS_SELECTOR, "#main h1")
    TOTAL_PRODUCTS = (By.CSS_SELECTOR, "#js-product-list-top .total-products")
    SORT_ORDER = (By.CSS_SELECTOR, "#js-product-list-top .products-sort-order")
    PRODUCTS = (By.CSS_SELECTOR, "#js-product-list .product-miniature")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "#js-product-list .product-miniature .price")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-title a")

    KEY_ELEMENTS = {
        "category block": CATEGORY_BLOCK,
        "page title": PAGE_TITLE,
        "total products": TOTAL_PRODUCTS,
        "sort order": SORT_ORDER,
        "product card": PRODUCTS,
        "product price": PRODUCT_PRICES,
    }

    def open_first_product(self) -> ProductPage:
        title = self.find_all(self.PRODUCTS)[0].find_element(*self.PRODUCT_TITLE)
        title.click()
        return ProductPage(self.driver, self.base_url)
