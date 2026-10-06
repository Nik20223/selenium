# Автотесты Selenium для PrestaShop (Page Object + Allure)

Домашние задания по курсу OTUS QA Python: тесты магазина PrestaShop переписаны на
паттерн Page Object, в проект добавлены логирование и отчётность Allure. Покрыты
сценарии: добавление и удаление товара в разделе администратора, регистрация
покупателя, переключение валют из верхнего меню, добавление товара в корзину и
вход/выход в админке.

## Требования

- Python 3.10+
- Запущенный магазин PrestaShop (локальный стенд на `http://localhost:8081`)
- Один из браузеров: Chrome, Firefox или Edge
  (драйверы подбираются автоматически через Selenium Manager)
- В магазине включены минимум две активные валюты (для тестов смены валюты)
- Allure CLI — только для просмотра HTML-отчёта (см. раздел «Allure-отчёт»)

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

| Опция        | По умолчанию             | Назначение                                   |
| ------------ | ------------------------ | -------------------------------------------- |
| `--url`      | `http://localhost:8081`  | Базовый URL тестируемого магазина PrestaShop  |
| `--browser`  | `chrome`                 | Браузер: `chrome`, `firefox` или `edge`       |
| `--headless` | выключено                | Запускать браузер без графического окна       |
| `--executor` | не задано                | Хост удалённого Selenium/Selenoid (порт 4444) |
| `--browser_version` | не задано         | Версия браузера на удалённом сервере          |

Во время прогона результаты для Allure складываются в `allure-results/`, а логи
пишутся в файл `automation.log`.

## Запуск на Selenoid

Тесты умеют работать и с удалённым Selenium-сервером: с опцией `--executor`
браузер запрашивается через `webdriver.Remote`, без неё запускается локально.

Selenoid и его UI поднимаются в отдельной сети, туда же кладётся конфиг
браузеров:

```bash
docker network create selenoid

docker run -d --name selenoid --network selenoid -p 4444:4444 \
  -e DOCKER_API_VERSION=1.40 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)/selenoid/browsers.json:/etc/selenoid/browsers.json:ro" \
  aerokube/selenoid:latest -container-network selenoid -limit 4

docker run -d --name selenoid-ui --network selenoid -p 8090:8080 \
  aerokube/selenoid-ui:1.10.11 --selenoid-uri http://selenoid:4444
```

Браузеры описаны в `selenoid/browsers.json`:

| Браузер   | Версия | Образ                    |
| --------- | ------ | ------------------------ |
| `chrome`  | 120.0  | `selenoid/chrome:120.0`  |
| `firefox` | 120.0  | `selenoid/firefox:120.0` |

Образы браузеров Selenoid скачивает сам при первом запросе сессии. Прогон на
удалённых браузерах:

```bash
pytest --url http://prestashop --browser chrome  --executor localhost
pytest --url http://prestashop --browser firefox --executor localhost
```

Адрес магазина должен быть доступен **изнутри браузера**, то есть из сети
`selenoid`, поэтому в примерах стоит `http://prestashop`, а не `localhost`.
Опция `--browser_version` позволяет запросить конкретную версию браузера
вместо версии по умолчанию.

## Запуск в Docker

Проект собирается в образ, который запускает тесты через `pytest`:

```bash
docker build -t prestashop-tests .
docker run --rm --network host prestashop-tests --browser firefox
```

- `ENTRYPOINT ["pytest", "--headless"]` — в контейнере нет дисплея, поэтому
  headless включён всегда. Аргументы после имени образа **заменяют** `CMD`,
  поэтому любые опции из `conftest.py` (`--browser`, `--url`) передаются как
  обычно: `docker run --rm --network host prestashop-tests --browser firefox`.
- В образ установлены и Chrome, и Firefox, поэтому работают оба варианта опции
  `--browser`.
- `--network host` нужен, чтобы контейнер видел магазин по тому же адресу, что
  прописан в настройках стенда (`PS_DOMAIN=localhost:8081`): иначе ссылки,
  которые генерирует PrestaShop, будут вести на `localhost` самого контейнера.
  Если host-сеть недоступна, укажите адрес явно:
  `docker run --rm --add-host=host.docker.internal:host-gateway prestashop-tests --url http://host.docker.internal:8081`.
- `CHROME_ARGS` в `Dockerfile` добавляет Chrome флаги `--no-sandbox` и
  `--disable-dev-shm-usage`, без которых браузер в контейнере не стартует.
- Каталог `allure-results` остаётся внутри контейнера; чтобы забрать отчёт,
  смонтируйте его: `-v "$(pwd)/allure-results:/tests/allure-results"`.

## Структура проекта

```
.
├── Dockerfile                     # образ с Chrome и Firefox для запуска тестов
├── .dockerignore                  # что не попадает в контекст сборки
├── conftest.py                    # фикстуры, опции запуска, скриншот при падении
├── pytest.ini                     # конфигурация pytest, логирование, --alluredir
├── requirements.txt               # зависимости проекта
├── pages/                         # Page Object Model
│   ├── base_page.py               # ожидания, навигация, логирование, смена валюты
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

## Логирование

Логирование построено на стандартном модуле `logging`. Каждый Page Object получает
собственный логгер в `BasePage.__init__`:

```python
self.logger = logging.getLogger(type(self).__name__)
```

Логи пишутся как в базовых действиях Page Object-ов (`open`, `find`, `click`,
`switch_currency`), так и в бизнес-методах (`login`, `register`, `add_to_cart`,
`delete_product`, `save`), поэтому по логу видно, что именно делал тест в браузере.

Настройки заданы в `pytest.ini`:

- вывод в консоль (`log_cli`) на уровне `INFO`;
- запись в файл `automation.log` на уровне `DEBUG`.

Пример записей:

```
10:15:03 [INFO] MainPage: Открываю страницу http://localhost:8081/
10:15:04 [INFO] MainPage: Кликаю по элементу ('css selector', ".product-title a")
```

Захваченный во время теста лог автоматически прикладывается к результату Allure.

## Allure-отчёт

Тесты и шаги размечены аннотациями Allure: `@allure.feature`, `@allure.story`,
`@allure.title`, `@allure.severity` на тестах и `@allure.step` на методах
Page Object-ов. Шаги Page Object-ов попадают в отчёт как отдельные шаги с
параметрами (например, «Зарегистрировать пользователя user@example.com»).

Результаты запуска (`allure-results/`) формируются автоматически при `pytest` —
за это отвечает `addopts` в `pytest.ini`. Для сборки HTML-отчёта нужен Allure CLI
(ставится по инструкции <https://allurereport.org/docs/install/>; например,
`scoop install allure` в Windows или `brew install allure` в macOS — классический
Allure 2 требует установленной Java):

```bash
allure serve allure-results                                    # собрать и открыть отчёт
allure generate allure-results -o allure-report --clean        # собрать в папку
```

## Скриншоты при падении

Хук `pytest_runtest_makereport` в `conftest.py` перехватывает падение теста, снимает
скриншот через `driver.get_screenshot_as_png()` и прикрепляет его к отчёту Allure
(`allure.attach`, тип `image/png`):

```python
allure.attach(
    driver.get_screenshot_as_png(),
    name="screenshot-on-failure",
    attachment_type=allure.attachment_type.PNG,
)
```

## Покрытие

### Наличие элементов на страницах

| Тест                              | Страница                            |
| --------------------------------- | ----------------------------------- |
| `tests/test_main_page.py`         | Главная                             |
| `tests/test_catalog_page.py`      | Каталог (`/9-art`)                  |
| `tests/test_product_page.py`      | Карточка товара                     |
| `tests/test_admin_login_page.py`  | Вход в админку (`/administration`)  |
| `tests/test_registration_page.py` | Регистрация (`/registration`)       |

Для каждой страницы проверяется не менее пяти ключевых элементов с помощью явных
ожиданий (`WebDriverWait` + `expected_conditions`).

### Сценарии

| Тест                                                                   | Сценарий                                                  |
| ---------------------------------------------------------------------- | --------------------------------------------------------- |
| `tests/test_admin_products.py::test_admin_can_add_product`             | Добавление нового товара в разделе администратора         |
| `tests/test_admin_products.py::test_admin_can_delete_product`          | Удаление товара из списка в разделе администратора        |
| `tests/test_registration.py::test_customer_can_register`               | Регистрация нового пользователя в магазине PrestaShop     |
| `tests/test_currency.py::test_currency_can_be_switched_from_top_menu`  | Переключение валют из верхнего меню PrestaShop            |
| `tests/test_currency.py::test_currency_changes_prices_on_main_page`    | Смена валюты меняет цены на главной                       |
| `tests/test_currency.py::test_currency_changes_prices_on_catalog_page` | Смена валюты меняет цены в каталоге                       |
| `tests/test_add_to_cart.py`                                            | Добавление случайного товара с главной и проверка корзины |
| `tests/test_admin_login_logout.py::test_admin_can_login_and_logout`    | Логин и разлогин в админку                                |

## Учётные данные администратора

Для сценариев в админке используется демонстрационный администратор стенда:

- e-mail: `admin@example.com`
- пароль: `Admin123!`

## Проверка

Все 13 тестов проходят на локальном стенде PrestaShop 8.2.7 (тема `classic`) в
headless Chrome:

```
13 passed
```

Селекторы выверены по реальному markup работающего магазина, а не только по
шаблонам темы.
