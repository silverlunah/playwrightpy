import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
from constants.common import STANDARD_USER, NAV_TITLE

# Load environment variables
load_dotenv()

# String variables
HOMEPAGE_URL = os.getenv("HOMEPAGE_URL")
INVENTORY_URL = HOMEPAGE_URL + "inventory.html"
EXPECTED_PRICES = {
    "Sauce Labs Backpack": "$29.99",
    "Sauce Labs Bike Light": "$9.99",
    "Sauce Labs Bolt T-Shirt": "$15.99",
    "Sauce Labs Fleece Jacket": "$49.99",
    "Sauce Labs Onesie": "$7.99",
    "Test.allTheThings() T-Shirt (Red)": "$15.99"
}

# Xpaths
LOGIN_INPUT_XPATH = "//input[@id='user-name']"
PASSWORD_INPUT_XPATH = "//input[@id='password']"

# CSS Selectors
SUBMIT_BUTTON_CSS = "input[type='submit']"
LOGOUT_BUTTON_CSS = "a#logout_sidebar_link"
MENU_ICON_CSS = "button#react-burger-menu-btn"
PRODUCT_CARD_CSS = ".inventory_item"
PRODUCT_TITLE_CSS = ".inventory_item_name"
PRODUCT_PRICE_CSS = ".inventory_item_price"

# Global fixture
@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        # Chromium in headful mode
        browser = p.chromium.launch(args=['--start-maximized'], headless=False)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        yield page
        browser.close()

# Test cases
@pytest.mark.login  # Test the login functionality
def test_login(browser):
    # Go to the homepage URL
    browser.goto(HOMEPAGE_URL)
    
    # Fill out login form using XPath selector
    browser.fill(LOGIN_INPUT_XPATH, STANDARD_USER["USERNAME"])
    browser.fill(PASSWORD_INPUT_XPATH, STANDARD_USER["PASSWORD"])
    
    # Click login button using CSS selector
    browser.click(SUBMIT_BUTTON_CSS)
    
    # Wait for the URL to change after login
    browser.wait_for_url(INVENTORY_URL)
    
    # Check if logged in by verifying the browser title
    assert browser.title() == NAV_TITLE

@pytest.mark.logout # Test the logout functionality
def test_logout(browser):
    # Go to the homepage URL
    browser.goto(HOMEPAGE_URL)
    
    # Fill in the login form using XPath selector
    browser.fill(LOGIN_INPUT_XPATH, STANDARD_USER["USERNAME"])
    browser.fill(PASSWORD_INPUT_XPATH, STANDARD_USER["PASSWORD"])
    
    # Click the login button using CSS selector
    browser.click(SUBMIT_BUTTON_CSS)

    # Wait for the inventory page to load
    browser.wait_for_url(INVENTORY_URL)

    # Click hamburger menu using CSS selector
    browser.click(MENU_ICON_CSS)
    
    # Simulate clicking the logout button using CSS selector
    browser.click(LOGOUT_BUTTON_CSS)
    
    # Wait for the page to return to the login screen
    browser.wait_for_url(HOMEPAGE_URL)
    
    # Assert that the page title is correct after logout
    assert browser.title() == NAV_TITLE

@pytest.mark.checkPrices # Assert the prices if correct according to the file
def test_prices(browser):
    
    # Go to the homepage URL
    browser.goto(HOMEPAGE_URL)
    
    # Fill in the login form using XPath selector
    browser.fill(LOGIN_INPUT_XPATH, STANDARD_USER["USERNAME"])
    browser.fill(PASSWORD_INPUT_XPATH, STANDARD_USER["PASSWORD"])
    
    # Click the login button using CSS selector
    browser.click(SUBMIT_BUTTON_CSS)
    
    # Wait for the inventory page to load
    browser.wait_for_url(INVENTORY_URL)
    
    # Get all product cards
    products = browser.query_selector_all(PRODUCT_CARD_CSS)

    # Initialize a list to store gathered prices from the UI
    ui_prices = {}

    # Get product name and price for each product
    for product in products:
        title = product.query_selector(PRODUCT_TITLE_CSS).inner_text()
        price = product.query_selector(PRODUCT_PRICE_CSS).inner_text()

        ui_prices[title] = price

    # To replicate soft assert, initialize a list to get failed assertions
    failed_assertions = []

    # Assert that the UI prices match the expected prices
    for product, expected_price in EXPECTED_PRICES.items():
        # Print the comparison: Value from UI vs Expected value
        ui_price = ui_prices.get(product)
        print(f"Asserting [{product}] price from UI: [{ui_price}] with expected value: [{expected_price}].")

        # Get assertion failure if there is a mismatch
        if ui_price != expected_price:
            failed_assertions.append(f"Price mismatch for {product}. Expected {expected_price}, but got {ui_price}")
    
    # After the loop, if there's' any failed assertions, print them out
    if failed_assertions:
        for failure in failed_assertions:
            print(failure)

    # Assert that no failures occurred (if any)
    assert not failed_assertions, f"Soft Assertion failed for the following products:\n" + "\n".join(failed_assertions)
