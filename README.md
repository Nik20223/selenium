# Автотесты Selenium для PrestaShop

Домашнее задание по теме «Написание простых автотестов и основы Selenium»
(курс OTUS QA Python, файл задания `selenium/hw.md`).

## Требования

- Python 3.10+
- Запущенный магазин PrestaShop (локальный стенд на `http://localhost:8081`)
- Один из браузеров: Chrome, Firefox или Edge
  (драйверы подбираются автоматически через Selenium Manager)

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
├── conftest.py         # фикстуры браузера и базового URL, опции командной строки
├── pytest.ini          # конфигурация pytest
├── requirements.txt    # зависимости проекта
├── pages/              # Page Object Model
└── tests/              # тесты
```

## Покрытие

### Часть 2. Наличие элементов на страницах

| Тест                                             | Страница                        |
| ------------------------------------------------ | ------------------------------- |
| `tests/test_main_page.py`                        | Главная                         |
| `tests/test_catalog_page.py`                     | Каталог (`/9-art`)              |
| `tests/test_product_page.py`                     | Карточка товара                 |
| `tests/test_admin_login_page.py`                 | Вход в админку (`/administration`) |
| `tests/test_registration_page.py`                | Регистрация (`/registration`)   |

Для каждой страницы проверяется не менее пяти ключевых элементов с помощью
явных ожиданий (`WebDriverWait` + `expected_conditions`).

### Часть 3. Сценарии

| Тест                                                          | Сценарий                                              |
| ------------------------------------------------------------- | ----------------------------------------------------- |
| `tests/test_admin_login_logout.py::test_admin_can_login_and_logout` | Логин и разлогин в админку                            |
| `tests/test_add_to_cart.py`                                   | Добавление случайного товара с главной и проверка корзины |
| `tests/test_currency.py::test_currency_changes_prices_on_main_page` | Смена валюты меняет цены на главной              |
| `tests/test_currency.py::test_currency_changes_prices_on_catalog_page` | Смена валюты меняет цены в каталоге           |

## Учётные данные администратора

Для сценария логина используется демонстрационный администратор стенда:

- e-mail: `admin@example.com`
- пароль: `Admin123!`
