from pages.catalog_page import CatalogPage


def test_catalog_page_elements(browser, base_url):
    CatalogPage(browser, base_url).open().assert_key_elements()
