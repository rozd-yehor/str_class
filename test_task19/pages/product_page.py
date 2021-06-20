from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:

    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self):
        self.driver.implicitly_wait(0)
        try:
            self.driver.find_element_by_xpath("//select[@name='options[Size]']").click()
            self.driver.find_element_by_xpath("//option[@value][2]").click()
            self.driver.implicitly_wait(10)
        except NoSuchElementException:
            self.driver.implicitly_wait(10)
        initial_quantity = self.driver.find_element_by_xpath("//span[@class='quantity']").text
        self.new_quantity = str(int(initial_quantity) + 1)
        self.driver.find_element_by_xpath("//button[@name='add_cart_product']").click()
        return self.new_quantity

    def wait_number_of_products_changed(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//span[@class='quantity']"), self.new_quantity))

    def open_cart(self):
        self.driver.find_element_by_xpath("//a[contains(@href, 'checkout') and @class='link']").click()
