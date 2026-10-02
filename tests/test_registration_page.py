from pages.registration_page import RegistrationPage


def test_registration_page_elements(browser, base_url):
    RegistrationPage(browser, base_url).open().assert_key_elements()
