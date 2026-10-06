import uuid

import allure

from pages.registration_page import RegistrationPage

PASSWORD = "Str0ng!P@ssw0rd#2024"


@allure.feature("Магазин")
@allure.story("Регистрация")
@allure.title("Регистрация нового пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_customer_can_register(browser, base_url):
    email = f"autotest_{uuid.uuid4().hex[:10]}@example.com"

    account = RegistrationPage(browser, base_url).open().register(
        "Auto", "Test", email, PASSWORD
    )

    with allure.step("Проверить, что пользователь вошёл в аккаунт"):
        assert account.account_name() == "Auto Test", (
            "Новый пользователь не зарегистрирован"
        )
