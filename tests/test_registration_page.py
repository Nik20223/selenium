import allure

from pages.registration_page import RegistrationPage


@allure.feature("Магазин")
@allure.story("Регистрация")
@allure.title("Наличие ключевых элементов на странице регистрации")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_page_elements(browser, base_url):
    RegistrationPage(browser, base_url).open().assert_key_elements()
