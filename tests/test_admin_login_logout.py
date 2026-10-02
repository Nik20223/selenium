from pages.admin_login_page import AdminLoginPage


def test_admin_can_login_and_logout(browser, base_url, admin_credentials):
    email, password = admin_credentials
    login_page = AdminLoginPage(browser, base_url).open()

    dashboard = login_page.login(email, password)
    assert dashboard.is_logged_in(), "Не удалось войти в админку"

    dashboard.logout()
    assert login_page.is_visible(AdminLoginPage.SUBMIT), "Не удалось выйти из админки"
