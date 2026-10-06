import allure

from pages.catalog_page import CatalogPage


@allure.feature("Магазин")
@allure.story("Карточка товара")
@allure.title("Наличие ключевых элементов на странице товара")
@allure.severity(allure.severity_level.NORMAL)
def test_product_page_elements(browser, base_url):
    CatalogPage(browser, base_url).open().open_first_product().assert_key_elements()
