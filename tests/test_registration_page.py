from pages.registration_page import RegistrationPage


def test_registration_page_elements(browser, base_url):
    page = RegistrationPage(browser, base_url).open()

    for name, locator in RegistrationPage.KEY_ELEMENTS.items():
        assert page.is_visible(locator), f"Элемент '{name}' не найден на странице регистрации"
