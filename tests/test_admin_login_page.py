import allure

from pages.admin_login_page import AdminLoginPage


@allure.feature("Панель администратора")
@allure.story("Авторизация")
@allure.title("Наличие ключевых элементов на странице входа в админку")
@allure.severity(allure.severity_level.NORMAL)
def test_admin_login_page_elements(browser, base_url):
    AdminLoginPage(browser, base_url).open().assert_key_elements()
