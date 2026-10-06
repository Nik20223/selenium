from pages.admin_login_page import AdminLoginPage


def test_admin_login_page_elements(browser, base_url):
    AdminLoginPage(browser, base_url).open().assert_key_elements()
