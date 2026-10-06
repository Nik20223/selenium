from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    PATH = "/administration"

    EMPLOYEE_BOX = (By.CSS_SELECTOR, "#header_employee_box")
    EMPLOYEE_MENU = (By.CSS_SELECTOR, "#employee_infos a.employee_name")
    LOGOUT_LINK = (By.CSS_SELECTOR, "#header_logout")

    def is_logged_in(self) -> bool:
        return self.is_visible(self.EMPLOYEE_BOX)

    def logout(self) -> "AdminDashboardPage":
        self.click(self.EMPLOYEE_MENU)
        self.click(self.LOGOUT_LINK)
        return self
