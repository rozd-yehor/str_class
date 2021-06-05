import time
from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


def add_1st_product_to_cart(driver):
    driver.get("http://localhost/litecart/")
    driver.find_elements_by_xpath("//li[contains(@class, 'product')]")[0].click()
    driver.implicitly_wait(0)
    try:
        driver.find_element_by_xpath("//select[@name='options[Size]']").click()
        driver.find_element_by_xpath("//option[@value][2]").click()
        driver.implicitly_wait(10)
    except NoSuchElementException:
        driver.implicitly_wait(10)
    initial_quantity = driver.find_element_by_xpath("//span[@class='quantity']").text
    new_quantity = str(int(initial_quantity) + 1)
    driver.find_element_by_xpath("//button[@name='add_cart_product']").click()
    wait = WebDriverWait(driver, 5)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//span[@class='quantity']"), new_quantity))


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


def test_work_with_cart(driver):
    add_1st_product_to_cart(driver)
    add_1st_product_to_cart(driver)
    add_1st_product_to_cart(driver)
    driver.find_element_by_xpath("//a[contains(@href, 'checkout') and @class='link']").click()
    checkout_number_of_ducks = len(driver.find_elements_by_xpath("//li[@class='shortcut']"))
    for n in range(0, checkout_number_of_ducks):
        order_number_of_ducks = len(driver.find_elements_by_xpath("//td[@class='item']"))
        if n != checkout_number_of_ducks-1:
            driver.find_element_by_xpath("//li[@class='shortcut'][1]").click()
            driver.find_element_by_xpath("//button[@name='remove_cart_item'][1]").click()
        else:
            driver.find_element_by_xpath("//button[@name='remove_cart_item'][1]").click()
        for i in range(0, 10):
            driver.implicitly_wait(0)
            if len(driver.find_elements_by_xpath("//td[@class='item']")) == order_number_of_ducks - 1:
                driver.implicitly_wait(10)
                break
            else:
                time.sleep(0.5)
        else:
            raise AssertionError
    driver.find_element_by_xpath("//em[contains(text(), 'no items')]")
