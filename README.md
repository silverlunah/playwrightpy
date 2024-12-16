### Summary
A simple Playeright test script for https://saucedemo.com/ written in Python showcasing basic test automation techniques such as:

- Test Annotations
- Selectors (xpath and css selector)
- Constant (dictionary) file
- .env file
- Soft Assertions

### Installation
  Clone or download project to your local:
  - `https://github.com/silverlunah/playwrightpy.git`
    
  If not yet installed:
  - `pip install pytest-playwright`
  - `playwright install`

  dotenv:
  - `pip install python-dotenv`

### Running tests:
There are three test cases included in this script and they can be run each using:
- `pytest -m login -s`
- `pytest -m logout -s`
- `pytest -m checkPrices -s`

Login and logout are simple test cases, but the checkPrices test case includes a loop that will assert the prices of each product in the Inventory page using soft assertion against a predefined expected output variable.

This test will log all the assertions executed and of course, the failing assertions.
