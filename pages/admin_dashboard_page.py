import allure
from selenium.webdriver.common.by import By

from pages.admin_products_page import AdminProductsPage
from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    PATH = "/administration"

    EMPLOYEE_BOX = (By.CSS_SELECTOR, "#header_employee_box")
    EMPLOYEE_MENU = (By.CSS_SELECTOR, "#employee_infos a.employee_name")
    LOGOUT_LINK = (By.CSS_SELECTOR, "#header_logout")

    def is_logged_in(self) -> bool:
        return self.is_visible(self.EMPLOYEE_BOX)

    @allure.step("Открыть список товаров")
    def open_products(self) -> AdminProductsPage:
        """Open the product catalog from the back-office menu."""
        return AdminProductsPage(self.driver, self.base_url).open()

    @allure.step("Выйти из панели администратора")
    def logout(self) -> "AdminDashboardPage":
        self.click(self.EMPLOYEE_MENU)
        self.click(self.LOGOUT_LINK)
        self.logger.info("Выполнен выход из админки")
        return self
