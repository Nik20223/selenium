from pages.main_page import MainPage


def test_main_page_elements(browser, base_url):
    MainPage(browser, base_url).open().assert_key_elements()
