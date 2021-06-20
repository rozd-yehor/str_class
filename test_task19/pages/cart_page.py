import time
from selenium.common.exceptions import NoSuchElementException


class CartPage:

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("http://localhost/litecart/checkout")

    def delete_all_products(self):
        initial_order_number_of_ducks = len(self.driver.find_elements_by_xpath("//td[@class='item']"))
        for n in range(0, initial_order_number_of_ducks):
            changing_order_number_of_ducks = len(self.driver.find_elements_by_xpath("//td[@class='item']"))
            try:
                self.driver.implicitly_wait(0)
                self.driver.find_element_by_xpath("//li[@class='shortcut'][1]").click()
                self.driver.find_element_by_xpath("//button[@name='remove_cart_item'][1]").click()
            except NoSuchElementException:
                self.driver.find_element_by_xpath("//button[@name='remove_cart_item'][1]").click()
            for i in range(0, 10):
                if len(self.driver.find_elements_by_xpath("//td[@class='item']")) == changing_order_number_of_ducks - 1:
                    self.driver.implicitly_wait(10)
                    break
                else:
                    time.sleep(0.5)
            else:
                raise AssertionError
        self.driver.find_element_by_xpath("//em[contains(text(), 'no items')]")
