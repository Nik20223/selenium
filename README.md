# Автотесты Selenium для PrestaShop (Page Object)

Домашнее задание по теме «PageObject» (курс OTUS QA Python, файл задания
`pageobject/hw.md`). Тесты магазина PrestaShop переписаны на паттерн Page Object,
добавлены сценарии: добавление товара в разделе администратора, удаление товара из
списка, регистрация нового покупателя и переключение валют из верхнего меню.

## Требования

- Python 3.10+
- Запущенный магазин PrestaShop (локальный стенд на `http://localhost:8081`)
- Один из браузеров: Chrome, Firefox или Edge
  (драйверы подбираются автоматически через Selenium Manager)
- В магазине включены минимум две активные валюты (для тестов смены валюты)

## Установка

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
pytest --url http://localhost:8081 --browser chrome
```

Опции командной строки:

| Опция       | По умолчанию             | Назначение                                  |
| ----------- | ------------------------ | ------------------------------------------- |
| `--url`     | `http://localhost:8081`  | Базовый URL тестируемого магазина PrestaShop |
| `--browser` | `chrome`                 | Браузер: `chrome`, `firefox` или `edge`      |
| `--headless`| выключено                | Запускать браузер без графического окна      |

## Структура проекта

```
.
├── conftest.py                    # фикстуры браузера, базового URL, опции запуска
├── pytest.ini                     # конфигурация pytest
├── requirements.txt               # зависимости проекта
├── pages/                         # Page Object Model
│   ├── base_page.py               # общие ожидания, навигация, смена валюты
│   ├── main_page.py               # главная
│   ├── catalog_page.py            # каталог
│   ├── product_page.py            # карточка товара
│   ├── cart_page.py               # корзина
│   ├── registration_page.py       # регистрация покупателя
│   ├── admin_login_page.py        # вход в админку
│   ├── admin_dashboard_page.py    # дашборд админки
│   ├── admin_products_page.py     # список товаров в админке
│   └── admin_product_form_page.py # форма товара в админке
└── tests/                         # тесты
```

Каждая страница — отдельный класс с локаторами и методами-действиями; тесты не
содержат селекторов и работают только через эти методы.

## Покрытие

### Наличие элементов на страницах

| Тест                          | Страница                                    |
| ----------------------------- | ------------------------------------------- |
| `tests/test_main_page.py`     | Главная                                     |
| `tests/test_catalog_page.py`  | Каталог (`/9-art`)                          |
| `tests/test_product_page.py`  | Карточка товара                             |
| `tests/test_admin_login_page.py` | Вход в админку (`/administration`)        |
| `tests/test_registration_page.py` | Регистрация (`/registration`)            |

Для каждой страницы проверяется не менее пяти ключевых элементов с помощью
явных ожиданий (`WebDriverWait` + `expected_conditions`).

### Сценарии

| Тест                                                                  | Сценарий                                                   |
| --------------------------------------------------------------------- | ---------------------------------------------------------- |
| `tests/test_admin_products.py::test_admin_can_add_product`            | Добавление нового товара в разделе администратора          |
| `tests/test_admin_products.py::test_admin_can_delete_product`         | Удаление товара из списка в разделе администратора         |
| `tests/test_registration.py::test_customer_can_register`              | Регистрация нового пользователя в магазине PrestaShop      |
| `tests/test_currency.py::test_currency_can_be_switched_from_top_menu` | Переключение валют из верхнего меню PrestaShop             |
| `tests/test_currency.py::test_currency_changes_prices_on_main_page`   | Смена валюты меняет цены на главной                        |
| `tests/test_currency.py::test_currency_changes_prices_on_catalog_page`| Смена валюты меняет цены в каталоге                        |
| `tests/test_add_to_cart.py`                                           | Добавление случайного товара с главной и проверка корзины  |
| `tests/test_admin_login_logout.py::test_admin_can_login_and_logout`   | Логин и разлогин в админку                                 |

## Учётные данные администратора

Для сценариев в админке используется демонстрационный администратор стенда:

- e-mail: `admin@example.com`
- пароль: `Admin123!`

## Проверка

Все 13 тестов проходят на локальном стенде PrestaShop 8.2.7 (тема `classic`)
в headless Chrome:

```
13 passed
```

Селекторы выверены по реальному markup работающего магазина, а не только по
шаблонам темы.
