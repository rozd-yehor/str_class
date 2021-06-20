class MainPage:

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("http://localhost/litecart/")

    def open_first_product(self):
        self.driver.find_elements_by_xpath("//li[contains(@class, 'product')]")[0].click()
