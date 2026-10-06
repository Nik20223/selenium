from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AdminProductFormPage(BasePage):
    """Product edit form in the back office."""

    NAME = (By.CSS_SELECTOR, "#product_header_name_1")
    SAVE = (By.CSS_SELECTOR, "#product_footer_save")

    def set_name(self, name: str) -> "AdminProductFormPage":
        field = self.find(self.NAME)
        field.clear()
        field.send_keys(name)
        return self

    def name(self) -> str:
        return self.find(self.NAME).get_attribute("value").strip()

    def save(self) -> "AdminProductFormPage":
        """Save the product; the button disables again once the form is saved."""
        self.click(self.SAVE)
        self.wait.until_not(EC.element_to_be_clickable(self.SAVE))
        return self
