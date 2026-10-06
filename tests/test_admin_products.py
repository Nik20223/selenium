import uuid

from pages.admin_login_page import AdminLoginPage


def _login(browser, base_url, credentials):
    email, password = credentials
    return AdminLoginPage(browser, base_url).open().login(email, password)


def _unique_product_name() -> str:
    return f"Auto test {uuid.uuid4().hex[:8]}"


def test_admin_can_add_product(browser, base_url, admin_credentials):
    name = _unique_product_name()
    products = _login(browser, base_url, admin_credentials).open_products()

    products.start_adding_product().set_name(name).save()

    products.open()
    assert name in products.product_names(), f"Товар '{name}' не появился в списке"


def test_admin_can_delete_product(browser, base_url, admin_credentials):
    name = _unique_product_name()
    products = _login(browser, base_url, admin_credentials).open_products()

    products.start_adding_product().set_name(name).save()
    products.open()
    assert name in products.product_names(), f"Товар '{name}' не создан для удаления"

    products.delete_product(name)

    assert name not in products.product_names(), f"Товар '{name}' не удалился"
