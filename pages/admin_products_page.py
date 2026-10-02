import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.admin_product_form_page import AdminProductFormPage
from pages.base_page import BasePage


class AdminProductsPage(BasePage):
    """Product catalog (grid) in the back office."""

    MENU_LINK = (By.CSS_SELECTOR, "#subtab-AdminProducts a")
    GRID = (By.CSS_SELECTOR, "#product_grid_table")
    ROWS = (By.CSS_SELECTOR, "#product_grid_table tbody tr")
    ROW_NAME = (By.CSS_SELECTOR, ".column-name a")
    ROW_ACTIONS_TOGGLE = (By.CSS_SELECTOR, ".dropdown-toggle-dots")
    ROW_DELETE = (By.CSS_SELECTOR, "a.grid-delete-row-link")

    ADD_PRODUCT = (By.CSS_SELECTOR, "#page-header-desc-configuration-add")
    CREATE_FRAME = (By.CSS_SELECTOR, "iframe[name='modal-create-product-iframe']")
    CREATE_SUBMIT = (By.CSS_SELECTOR, "#create_product_create")

    CONFIRM_DELETE = (By.CSS_SELECTOR, ".modal.show .btn-confirm-submit")

    KEY_ELEMENTS = {
        "products grid": GRID,
        "add product button": ADD_PRODUCT,
    }

    @allure.step("Открыть список товаров")
    def open(self) -> "AdminProductsPage":
        """Open the products grid through the back-office menu."""
        link = self.wait.until(EC.presence_of_element_located(self.MENU_LINK))
        self.logger.info("Открываю список товаров: %s", link.get_attribute("href"))
        self.driver.get(link.get_attribute("href"))
        self.find(self.GRID)
        return self

    def product_names(self) -> list[str]:
        return [
            row.find_element(*self.ROW_NAME).text.strip()
            for row in self.find_all(self.ROWS)
        ]

    @allure.step("Начать создание нового товара")
    def start_adding_product(self) -> AdminProductFormPage:
        """Open the 'New product' modal and create a standard product."""
        self.click(self.ADD_PRODUCT)
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME))
        self.click(self.CREATE_SUBMIT)
        self.driver.switch_to.default_content()
        return AdminProductFormPage(self.driver, self.base_url)

    @allure.step("Удалить товар {name}")
    def delete_product(self, name: str) -> "AdminProductsPage":
        """Delete the product with the given name from the grid."""
        row = self._row(name)
        row.find_element(*self.ROW_ACTIONS_TOGGLE).click()
        delete_link = row.find_element(*self.ROW_DELETE)
        self.wait.until(EC.visibility_of(delete_link)).click()
        self.click(self.CONFIRM_DELETE)
        self.wait.until(lambda _: name not in self.product_names())
        self.logger.info("Товар удалён: %s", name)
        return self

    def _row(self, name: str):
        for row in self.find_all(self.ROWS):
            if row.find_element(*self.ROW_NAME).text.strip() == name:
                return row
        raise AssertionError(f"Товар '{name}' не найден в списке")
