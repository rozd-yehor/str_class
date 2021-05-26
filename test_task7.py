import time
from _pytest.fixtures import fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("credentials_enable_service", False)
    # chrome_options.add_experimental_option("password_manager_enabled", False)
    wd = webdriver.Chrome(options=chrome_options)
    wd.implicitly_wait(10)
    yield wd
    wd.quit()


def test_open_google(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    time.sleep(100)
