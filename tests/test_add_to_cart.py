from pages.cart_page import CartPage
from pages.main_page import MainPage


def test_add_random_product_from_main_page_to_cart(browser, base_url):
    main_page = MainPage(browser, base_url).open()
    product_page = main_page.open_random_product()
    # Listing titles are truncated by the theme; the product page shows the full name.
    product_name = product_page.name()

    product_page.add_to_cart()

    cart_page = CartPage(browser, base_url).open()
    # The theme changes the letter case with CSS, so compare case-insensitively.
    cart_products = [name.strip().casefold() for name in cart_page.product_names()]

    assert product_name.strip().casefold() in cart_products, (
        f"Товар '{product_name}' не появился в корзине: {cart_products}"
    )
