from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Shared navigation, explicit waits and header (currency) helpers."""

    PATH = "/"
    DEFAULT_TIMEOUT = 15

    CURRENCY_SELECTOR = (By.CSS_SELECTOR, ".currency-selector")
    CURRENT_CURRENCY = (By.CSS_SELECTOR, ".currency-selector > span")
    CURRENCY_OPTION = (By.CSS_SELECTOR, ".currency-selector a")

    def __init__(self, driver, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> "BasePage":
        """Navigate to the page path relative to the shop base URL."""
        self.driver.get(f"{self.base_url}/{self.PATH.lstrip('/')}")
        return self

    def find(self, locator):
        """Wait until the element is visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Wait until all matching elements are present and return them."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator) -> bool:
        """Return True if the element becomes visible, False on timeout."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def currency_links(self) -> dict[str, str]:
        """Return a mapping of currency ISO code -> switch link."""
        return {
            link.text.split()[0]: link.get_attribute("href")
            for link in self.find_all(self.CURRENCY_OPTION)
        }

    def current_currency(self) -> str:
        return self.get_text(self.CURRENT_CURRENCY).split()[0]

    def switch_currency(self, iso: str) -> "BasePage":
        self.driver.get(self.currency_links()[iso])
        return self

    def another_currency(self) -> str:
        current = self.current_currency()
        for iso in self.currency_links():
            if iso != current:
                return iso
        raise AssertionError("В магазине включена только одна валюта")
