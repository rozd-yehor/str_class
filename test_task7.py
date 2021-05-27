from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_element_present(driver, xpath):
    driver.implicitly_wait(0)
    wait = WebDriverWait(driver, 0.5)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.implicitly_wait(10)
    except TimeoutException:
        driver.implicitly_wait(10)
        raise AssertionError("h1 is absent on the page")


@fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    wd = webdriver.Chrome(options=chrome_options)
    wd.implicitly_wait(10)
    yield wd
    wd.quit()


def test_check_headers(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    side_menus_len = len(driver.find_elements_by_xpath("//li[@id='app-']"))
    for n in range(0, side_menus_len):
        driver.find_elements_by_xpath("//li[@id='app-']")[n].click()
        is_element_present(driver, "//h1")
        driver.implicitly_wait(0.5)
        side_submenus_len = len(driver.find_elements_by_xpath("//ul[@class='docs']/li[@id]"))
        driver.implicitly_wait(10)
        for nn in range(1, side_submenus_len):
            driver.find_elements_by_xpath("//ul[@class='docs']/li[@id]")[nn].click()
            is_element_present(driver, "//h1")
