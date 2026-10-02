from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.main_page import MainPage


class RegistrationPage(BasePage):
    PATH = "/registration"

    PAGE_TITLE = (By.CSS_SELECTOR, "#main .page-header h1")
    FORM = (By.CSS_SELECTOR, "#customer-form")
    FIRST_NAME = (By.CSS_SELECTOR, "#field-firstname")
    LAST_NAME = (By.CSS_SELECTOR, "#field-lastname")
    EMAIL = (By.CSS_SELECTOR, "#field-email")
    PASSWORD = (By.CSS_SELECTOR, "#field-password")
    TERMS = (By.CSS_SELECTOR, "input[name='psgdpr']")
    PRIVACY = (By.CSS_SELECTOR, "input[name='customer_privacy']")
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

    def register(self, first_name, last_name, email, password) -> MainPage:
        """Fill the form, accept the agreements and submit the registration."""
        self.find(self.FIRST_NAME).send_keys(first_name)
        self.find(self.LAST_NAME).send_keys(last_name)
        self.find(self.EMAIL).send_keys(email)
        self.find(self.PASSWORD).send_keys(password)
        self._accept(self.TERMS)
        self._accept(self.PRIVACY)
        self.click(self.SUBMIT)
        self.wait.until(lambda driver: "registration" not in driver.current_url)
        return MainPage(self.driver, self.base_url)

    def _accept(self, locator) -> None:
        """Tick a consent checkbox.

        The checkbox is styled with CSS and its label contains links, so a normal
        click is unreliable; a scripted click toggles the input deterministically.
        """
        checkbox = self.driver.find_element(*locator)
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)
