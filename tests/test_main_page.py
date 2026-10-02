import allure

from pages.main_page import MainPage


@allure.feature("Магазин")
@allure.story("Главная страница")
@allure.title("Наличие ключевых элементов на главной странице")
@allure.severity(allure.severity_level.NORMAL)
def test_main_page_elements(browser, base_url):
    MainPage(browser, base_url).open().assert_key_elements()
