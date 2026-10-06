import allure

from pages.admin_login_page import AdminLoginPage


@allure.feature("Панель администратора")
@allure.story("Авторизация")
@allure.title("Вход и выход из панели администратора")
@allure.severity(allure.severity_level.CRITICAL)
def test_admin_can_login_and_logout(browser, base_url, admin_credentials):
    email, password = admin_credentials
    login_page = AdminLoginPage(browser, base_url).open()

    dashboard = login_page.login(email, password)
    with allure.step("Проверить, что вход выполнен"):
        assert dashboard.is_logged_in(), "Не удалось войти в админку"

    dashboard.logout()
    with allure.step("Проверить, что выход выполнен"):
        assert login_page.is_visible(AdminLoginPage.SUBMIT), "Не удалось выйти из админки"
