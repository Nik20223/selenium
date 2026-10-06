from pages.admin_login_page import AdminLoginPage


def test_admin_login_page_elements(browser, base_url):
    page = AdminLoginPage(browser, base_url).open()

    for name, locator in AdminLoginPage.KEY_ELEMENTS.items():
        assert page.is_visible(locator), f"Элемент '{name}' не найден на странице входа в админку"
