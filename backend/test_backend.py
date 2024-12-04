import allure
from selenium import webdriver


@allure.feature('UI Testing')
def test_ui_example():
    driver = webdriver.Chrome()
    driver.get("https://example.com")
    assert "Example Domain" in driver.title
    driver.quit()
