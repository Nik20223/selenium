from pages.catalog_page import CatalogPage


def test_product_page_elements(browser, base_url):
    CatalogPage(browser, base_url).open().open_first_product().assert_key_elements()
