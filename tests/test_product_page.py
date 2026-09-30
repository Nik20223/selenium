from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage


def test_product_page_elements(browser, base_url):
    page = CatalogPage(browser, base_url).open().open_first_product()

    for name, locator in ProductPage.KEY_ELEMENTS.items():
        assert page.is_visible(locator), f"Элемент '{name}' не найден на карточке товара"
