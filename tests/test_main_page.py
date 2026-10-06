from pages.main_page import MainPage


def test_main_page_elements(browser, base_url):
    page = MainPage(browser, base_url).open()

    for name, locator in MainPage.KEY_ELEMENTS.items():
        assert page.is_visible(locator), f"Элемент '{name}' не найден на главной странице"
