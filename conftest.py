import pytest
from selenium import webdriver

DEFAULT_BROWSER = "chrome"
DEFAULT_URL = "http://localhost:8081"
SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"

BROWSER_FACTORIES = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
    "edge": webdriver.Edge,
}


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default=DEFAULT_BROWSER,
        choices=SUPPORTED_BROWSERS,
        help="Browser to run the tests in.",
    )
    parser.addoption(
        "--url",
        default=DEFAULT_URL,
        help="Base URL of the PrestaShop shop under test.",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run the browser in headless mode.",
    )


def _browser_options(browser_name: str, headless: bool):
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        return options
    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        return options
    options = webdriver.EdgeOptions()
    if headless:
        options.add_argument("--headless=new")
    return options


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """Base URL of the shop, taken from the ``--url`` command line option."""
    return request.config.getoption("--url").rstrip("/")


@pytest.fixture
def browser(request):
    """Start the browser passed via ``--browser`` and close it after the test."""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = BROWSER_FACTORIES[browser_name](
        options=_browser_options(browser_name, headless)
    )
    driver.set_window_size(1920, 1080)

    yield driver

    driver.quit()


@pytest.fixture
def admin_credentials() -> tuple[str, str]:
    """E-mail and password of the demo back-office administrator."""
    return ADMIN_EMAIL, ADMIN_PASSWORD
