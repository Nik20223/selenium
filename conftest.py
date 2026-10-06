import logging
import os

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

DEFAULT_BROWSER = "chrome"
DEFAULT_URL = "http://localhost:8081"
SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")
SELENOID_PORT = 4444

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
    parser.addoption(
        "--executor",
        default=None,
        help="Host of a remote Selenium/Selenoid instance, e.g. ``selenoid``.",
    )
    parser.addoption(
        "--browser_version",
        default=None,
        help="Browser version to request from the remote executor.",
    )


def _browser_options(browser_name: str, headless: bool):
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        for argument in os.environ.get("CHROME_ARGS", "").split():
            options.add_argument(argument)
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
    executor = request.config.getoption("--executor")
    browser_version = request.config.getoption("--browser_version")
    # Selenoid starts the browser in its own container, so the ``--headless``
    # flag that the tests image passes unconditionally means nothing for it.
    headless = request.config.getoption("--headless") and not executor

    options = _browser_options(browser_name, headless)
    if browser_version:
        options.browser_version = browser_version

    if executor:
        driver = webdriver.Remote(
            command_executor=f"http://{executor}:{SELENOID_PORT}/wd/hub",
            options=options,
        )
    else:
        driver = BROWSER_FACTORIES[browser_name](options=options)

    driver.set_window_size(1920, 1080)

    yield driver

    driver.quit()


@pytest.fixture
def admin_credentials() -> tuple[str, str]:
    """E-mail and password of the demo back-office administrator."""
    return ADMIN_EMAIL, ADMIN_PASSWORD


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a test fails."""
    report = yield
    if report.failed and report.when in ("setup", "call"):
        driver = (getattr(item, "funcargs", None) or {}).get("browser")
        if driver is not None:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot-on-failure",
                    attachment_type=allure.attachment_type.PNG,
                )
            except WebDriverException as error:
                logging.getLogger(__name__).warning(
                    "Не удалось сделать скриншот: %s", error
                )
    return report
