import allure

from pages.catalog_page import CatalogPage


@allure.feature("Магазин")
@allure.story("Каталог")
@allure.title("Наличие ключевых элементов на странице каталога")
@allure.severity(allure.severity_level.NORMAL)
def test_catalog_page_elements(browser, base_url):
    CatalogPage(browser, base_url).open().assert_key_elements()
