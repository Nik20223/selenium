from pages.catalog_page import CatalogPage
from pages.main_page import MainPage


def test_currency_can_be_switched_from_top_menu(browser, base_url):
    page = MainPage(browser, base_url).open()
    target = page.another_currency()

    page.switch_currency(target)

    assert page.current_currency() == target, "Валюта в верхнем меню не переключилась"


def test_currency_changes_prices_on_main_page(browser, base_url):
    page = MainPage(browser, base_url).open()
    prices_before = page.product_prices()

    page.switch_currency(page.another_currency())

    assert page.product_prices() != prices_before, (
        "Цены на товары на главной странице не изменились при смене валюты"
    )


def test_currency_changes_prices_on_catalog_page(browser, base_url):
    page = CatalogPage(browser, base_url).open()
    prices_before = page.product_prices()

    page.switch_currency(page.another_currency())

    assert page.product_prices() != prices_before, (
        "Цены на товары в каталоге не изменились при смене валюты"
    )
