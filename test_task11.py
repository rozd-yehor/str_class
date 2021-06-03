import time
from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def generate_email():
    counter_file = open("additional_files\\test_task11_email_counter.txt", 'r')
    counter = counter_file.read()
    email = "autotest" + counter + "@email.com"
    counter = int(counter) + 1
    counter_file = open("additional_files\\test_task11_email_counter.txt", 'w')
    counter_file.write(str(counter))
    counter_file.close()
    return email


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


def test_reg_new_user(driver):
    driver.get("http://localhost/litecart/")
    driver.find_element_by_xpath("//div[@id='box-account-login']//a[contains(@href, 'create_account')]").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//input[@name='firstname']").send_keys("Mshklek")
    driver.find_element_by_xpath("//input[@name='lastname']").send_keys("Mshklekov")
    driver.find_element_by_xpath("//input[@name='address1']").send_keys("Test Street 123")
    driver.find_element_by_xpath("//input[@name='postcode']").send_keys("12345")
    driver.find_element_by_xpath("//input[@name='city']").send_keys("TestCity")
    driver.find_element_by_xpath("//span[contains(@id, 'select2-country_code')]").click()
    driver.find_element_by_xpath("//li[contains(@id, 'US')]").click()
    driver.find_element_by_xpath("//select[@name='zone_code']").click()
    driver.find_element_by_xpath("//option[@value='OH']").click()
    driver.find_element_by_xpath("//input[@name='phone']").send_keys("+10123456789")
    while True:
        driver.find_element_by_xpath("//input[@name='email']").clear()
        my_email = generate_email()
        driver.find_element_by_xpath("//input[@name='email']").send_keys(my_email)
        driver.find_element_by_xpath("//input[@name='password']").send_keys("test")
        driver.find_element_by_xpath("//input[@name='confirmed_password']").send_keys("test")
        driver.find_element_by_xpath("//button[@name='create_account']").click()
        driver.implicitly_wait(1)
        try:
            if driver.find_element_by_xpath(
                    "//div[contains(text(), 'email address already exists')]").is_displayed() == False:
                driver.implicitly_wait(10)
                break
            else:
                driver.execute_script("arguments[0].setAttribute('style', 'display: none;')",
                                      driver.find_element_by_xpath("//div[@id='notices-wrapper']"))
                continue
        except NoSuchElementException:
            driver.implicitly_wait(10)
            break
    # # this works slowly in case of existing emails
    # while True:
    #     driver.find_element_by_xpath("//input[@name='email']").clear()
    #     my_email = generate_email()
    #     driver.find_element_by_xpath("//input[@name='email']").send_keys(my_email)
    #     driver.find_element_by_xpath("//input[@name='password']").send_keys("test")
    #     driver.find_element_by_xpath("//input[@name='confirmed_password']").send_keys("test")
    #     driver.find_element_by_xpath("//button[@name='create_account']").click()
    #     driver.implicitly_wait(3)
    #     try:
    #         driver.find_element_by_xpath("//div[@id='box-account']//a[contains(@href, 'logout')]").click()
    #     except NoSuchElementException:
    #         continue
    #     driver.implicitly_wait(10)
    #     break
    driver.find_element_by_xpath("//div[@id='box-account']//a[contains(@href, 'logout')]").click()
    driver.find_element_by_xpath("//input[@name='email']").send_keys(my_email)
    driver.find_element_by_xpath("//input[@name='password']").send_keys("test")
    driver.find_element_by_xpath("//button[@name='login']").click()
    driver.find_element_by_xpath("//div[@id='box-account']//a[contains(@href, 'logout')]").click()



