from selenium.webdriver.common.by import By

from pages.admin_dashboard_page import AdminDashboardPage
from pages.base_page import BasePage


class AdminLoginPage(BasePage):
    PATH = "/administration"

    LOGO = (By.CSS_SELECTOR, "#logo")
    FORM = (By.CSS_SELECTOR, "#login_form")
    EMAIL = (By.CSS_SELECTOR, "#email")
    PASSWORD = (By.CSS_SELECTOR, "#passwd")
    SUBMIT = (By.CSS_SELECTOR, "#submit_login")

    KEY_ELEMENTS = {
        "logo": LOGO,
        "login form": FORM,
        "email field": EMAIL,
        "password field": PASSWORD,
        "submit button": SUBMIT,
    }

    def login(self, email: str, password: str) -> AdminDashboardPage:
        self.find(self.EMAIL).send_keys(email)
        self.find(self.PASSWORD).send_keys(password)
        self.click(self.SUBMIT)
        return AdminDashboardPage(self.driver, self.base_url)
