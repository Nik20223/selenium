from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    PATH = "/registration"

    PAGE_TITLE = (By.CSS_SELECTOR, "#main .page-header h1")
    FORM = (By.CSS_SELECTOR, "#customer-form")
    FIRST_NAME = (By.CSS_SELECTOR, "#field-firstname")
    LAST_NAME = (By.CSS_SELECTOR, "#field-lastname")
    EMAIL = (By.CSS_SELECTOR, "#field-email")
    PASSWORD = (By.CSS_SELECTOR, "#field-password")
    SUBMIT = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")

    KEY_ELEMENTS = {
        "page title": PAGE_TITLE,
        "registration form": FORM,
        "first name field": FIRST_NAME,
        "last name field": LAST_NAME,
        "email field": EMAIL,
        "password field": PASSWORD,
        "submit button": SUBMIT,
    }
