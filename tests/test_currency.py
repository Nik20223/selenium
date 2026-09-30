from pages.catalog_page import CatalogPage
from pages.main_page import MainPage


def test_currency_changes_prices_on_main_page(browser, base_url):
    page = MainPage(browser, base_url).open()
    prices_before = page.product_prices()

    page.switch_currency(page.another_currency())
    prices_after = page.product_prices()

    assert prices_before != prices_after, (
        "Цены на товары на главной странице не изменились при смене валюты"
    )


def test_currency_changes_prices_on_catalog_page(browser, base_url):
    page = CatalogPage(browser, base_url).open()
    prices_before = page.product_prices()

    page.switch_currency(page.another_currency())
    prices_after = page.product_prices()

    assert prices_before != prices_after, (
        "Цены на товары в каталоге не изменились при смене валюты"
    )
