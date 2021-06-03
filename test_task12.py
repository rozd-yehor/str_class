import os
import datetime
import time

from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


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


def test_add_product(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    driver.find_element_by_xpath("//a[contains(@href, 'catalog')]").click()
    driver.find_element_by_xpath("//a[contains(@href, 'edit_product')]").click()
    # General tab
    driver.find_element_by_xpath("//input[@type='radio' and @value='1']").click()
    driver.find_element_by_xpath("//input[@name='name[en]']").send_keys("test_duck")
    driver.find_element_by_xpath("//input[@name='code']").send_keys("test")
    driver.find_element_by_xpath("//input[@type='checkbox' and @value='1']").click()
    driver.find_element_by_xpath("//select[@name='default_category_id']").click()
    driver.find_element_by_xpath("//select[@name='default_category_id']//option[@value='1']").click()
    driver.find_element_by_xpath("//input[@value='1-3']").click()
    driver.find_element_by_xpath("//input[@name='quantity']").clear()
    driver.find_element_by_xpath("//input[@name='quantity']").send_keys("3")
    duck_path = os.getcwd() + "\\additional_files\\test_task11_image.jpg"
    driver.find_element_by_xpath("//input[@type='file']").send_keys(duck_path)
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    driver.find_element_by_xpath("//input[@name='date_valid_from']").send_keys(yesterday)
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    driver.find_element_by_xpath("//input[@name='date_valid_to']").send_keys(tomorrow)
    # Information tab
    driver.find_element_by_xpath("//a[@href='#tab-information']").click()
    driver.find_element_by_xpath("//select[@name='manufacturer_id']").click()
    driver.find_element_by_xpath("//select[@name='manufacturer_id']//option[@value='1']").click()
    driver.find_element_by_xpath("//input[@name='keywords']").send_keys("key word")
    driver.find_element_by_xpath("//input[@name='short_description[en]']").send_keys("desc")
    driver.find_element_by_xpath("//div[@class='trumbowyg-editor']").send_keys("full description")
    driver.find_element_by_xpath("//input[@name='head_title[en]']").send_keys("head title test")
    driver.find_element_by_xpath("//input[@name='meta_description[en]']").send_keys("meta description test")
    # Prices tab
    driver.find_element_by_xpath("//a[@href='#tab-prices']").click()
    driver.find_element_by_xpath("//input[@name='purchase_price']").clear()
    driver.find_element_by_xpath("//input[@name='purchase_price']").send_keys("10")
    driver.find_element_by_xpath("//select[@name='purchase_price_currency_code']").click()
    driver.find_element_by_xpath("//option[@value='USD']").click()
    driver.find_element_by_xpath("//input[@name='gross_prices[USD]']").clear()
    driver.find_element_by_xpath("//input[@name='gross_prices[USD]']").send_keys("1")
    driver.find_element_by_xpath("//button[@name='save']").click()
    # Check added duck and delete it
    driver.find_element_by_xpath("//a[text()='test_duck']").click()
    driver.find_element_by_xpath("//button[@name='delete']").click()
    driver.switch_to.alert.accept()
    driver.implicitly_wait(1)
    try:
        driver.find_element_by_xpath("//a[text()='test_duck']")
    except NoSuchElementException:
        driver.implicitly_wait(10)
