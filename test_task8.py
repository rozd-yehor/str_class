from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options


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


def test_check_stickers(driver):
    driver.get("http://localhost/litecart/")
    number_of_ducks = len(driver.find_elements_by_xpath("//a[contains(@title, 'Duck') and @class='link']"))
    for n in range(0, number_of_ducks):
        duck = driver.find_elements_by_xpath("//li[@class='product column shadow hover-light']")[n]
        number_of_duck_stickers = len(duck.find_elements_by_xpath(".//div[starts-with(@class, 'sticker')]"))
        if number_of_duck_stickers != 1:
            raise AssertionError("Number of duck's stickers is not equal to 1")