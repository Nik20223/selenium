from pages.admin_login_page import AdminLoginPage

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"


def test_admin_can_login_and_logout(browser, base_url):
    login_page = AdminLoginPage(browser, base_url).open()
    dashboard = login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)

    assert dashboard.is_logged_in(), "Не удалось войти в админку"

    dashboard.logout()

    assert login_page.is_visible(AdminLoginPage.SUBMIT), "Не удалось выйти из админки"
