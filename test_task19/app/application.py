from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from test_task19.pages.main_page import MainPage
from test_task19.pages.product_page import ProductPage
from test_task19.pages.cart_page import CartPage


class Application:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.implicitly_wait(10)

        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def work_with_cart(self):
        for n in range(0, 3):
            self.main_page.open()
            self.main_page.open_first_product()
            self.product_page.add_to_cart()
            self.product_page.wait_number_of_products_changed()
        self.product_page.open_cart()
        self.cart_page.delete_all_products()
