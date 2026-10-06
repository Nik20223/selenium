from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Shared navigation, explicit waits and storefront header helpers."""

    PATH = "/"
    DEFAULT_TIMEOUT = 15

    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-miniature .price")

    CURRENCY_TOGGLE = (
        By.CSS_SELECTOR,
        "#_desktop_currency_selector .currency-selector button",
    )
    CURRENT_CURRENCY = (
        By.CSS_SELECTOR,
        "#_desktop_currency_selector .currency-selector button span",
    )
    CURRENCY_OPTION = (
        By.CSS_SELECTOR,
        "#_desktop_currency_selector .currency-selector .dropdown-menu a",
    )

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

    def assert_key_elements(self) -> None:
        """Assert that every locator declared in ``KEY_ELEMENTS`` is visible."""
        for label, locator in self.KEY_ELEMENTS.items():
            assert self.is_visible(locator), (
                f"Элемент '{label}' не найден на странице {type(self).__name__}"
            )

    def product_prices(self) -> list[str]:
        """Text of every product price shown on the page."""
        return [element.text for element in self.find_all(self.PRODUCT_PRICES)]

    def currency_links(self) -> dict[str, str]:
        """Return a mapping of currency ISO code -> switch link."""
        return {
            self._text(link).split()[0]: link.get_attribute("href")
            for link in self.find_all(self.CURRENCY_OPTION)
        }

    def current_currency(self) -> str:
        return self.get_text(self.CURRENT_CURRENCY).split()[0]

    def switch_currency(self, iso: str) -> "BasePage":
        """Switch the shop currency through the header dropdown menu."""
        self.click(self.CURRENCY_TOGGLE)
        for link in self.find_all(self.CURRENCY_OPTION):
            if self._text(link).split()[0] == iso:
                link.click()
                break
        else:
            raise AssertionError(f"Валюта '{iso}' не найдена в меню")
        self.wait.until(
            EC.text_to_be_present_in_element(self.CURRENT_CURRENCY, iso)
        )
        return self

    def another_currency(self) -> str:
        current = self.current_currency()
        for iso in self.currency_links():
            if iso != current:
                return iso
        raise AssertionError("В магазине включена только одна валюта")

    @staticmethod
    def _text(element) -> str:
        """Text of an element, including ones hidden inside a dropdown."""
        return (element.get_attribute("textContent") or "").strip()
