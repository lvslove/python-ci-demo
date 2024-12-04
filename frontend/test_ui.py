from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@allure.feature('UI Testing')
def test_ui_example():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://example.com")
    assert "Example Domain" in driver.title
    driver.quit()
