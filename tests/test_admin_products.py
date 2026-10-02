import uuid

import allure

from pages.admin_login_page import AdminLoginPage


def _login(browser, base_url, credentials):
    email, password = credentials
    return AdminLoginPage(browser, base_url).open().login(email, password)


def _unique_product_name() -> str:
    return f"Auto test {uuid.uuid4().hex[:8]}"


@allure.feature("Панель администратора")
@allure.story("Товары")
@allure.title("Добавление нового товара в разделе администратора")
@allure.severity(allure.severity_level.CRITICAL)
def test_admin_can_add_product(browser, base_url, admin_credentials):
    name = _unique_product_name()
    products = _login(browser, base_url, admin_credentials).open_products()

    products.start_adding_product().set_name(name).save()

    products.open()
    with allure.step(f"Проверить, что товар '{name}' появился в списке"):
        assert name in products.product_names(), f"Товар '{name}' не появился в списке"


@allure.feature("Панель администратора")
@allure.story("Товары")
@allure.title("Удаление товара из списка в разделе администратора")
@allure.severity(allure.severity_level.CRITICAL)
def test_admin_can_delete_product(browser, base_url, admin_credentials):
    name = _unique_product_name()
    products = _login(browser, base_url, admin_credentials).open_products()

    products.start_adding_product().set_name(name).save()
    products.open()
    with allure.step(f"Проверить, что товар '{name}' создан"):
        assert name in products.product_names(), f"Товар '{name}' не создан для удаления"

    products.delete_product(name)

    with allure.step(f"Проверить, что товар '{name}' удалён"):
        assert name not in products.product_names(), f"Товар '{name}' не удалился"
