from pages.catalog_page import CatalogPage


def test_catalog_page_elements(browser, base_url):
    page = CatalogPage(browser, base_url).open()

    for name, locator in CatalogPage.KEY_ELEMENTS.items():
        assert page.is_visible(locator), f"Элемент '{name}' не найден в каталоге"
