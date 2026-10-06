import allure

from pages.catalog_page import CatalogPage
from pages.main_page import MainPage


@allure.feature("Магазин")
@allure.story("Валюты")
@allure.title("Переключение валюты из верхнего меню")
@allure.severity(allure.severity_level.CRITICAL)
def test_currency_can_be_switched_from_top_menu(browser, base_url):
    page = MainPage(browser, base_url).open()
    target = page.another_currency()

    page.switch_currency(target)

    with allure.step(f"Проверить, что активна валюта {target}"):
        assert page.current_currency() == target, "Валюта в верхнем меню не переключилась"


@allure.feature("Магазин")
@allure.story("Валюты")
@allure.title("Смена валюты меняет цены на главной странице")
@allure.severity(allure.severity_level.NORMAL)
def test_currency_changes_prices_on_main_page(browser, base_url):
    page = MainPage(browser, base_url).open()
    prices_before = page.product_prices()

    page.switch_currency(page.another_currency())

    with allure.step("Проверить, что цены изменились"):
        assert page.product_prices() != prices_before, (
            "Цены на товары на главной странице не изменились при смене валюты"
        )


@allure.feature("Магазин")
@allure.story("Валюты")
@allure.title("Смена валюты меняет цены в каталоге")
@allure.severity(allure.severity_level.NORMAL)
def test_currency_changes_prices_on_catalog_page(browser, base_url):
    page = CatalogPage(browser, base_url).open()
    prices_before = page.product_prices()

    page.switch_currency(page.another_currency())

    with allure.step("Проверить, что цены изменились"):
        assert page.product_prices() != prices_before, (
            "Цены на товары в каталоге не изменились при смене валюты"
        )
