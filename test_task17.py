from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options


@fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_goods_browser_messages(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    driver.find_element_by_xpath("//a[contains(@href, 'catalog')]").click()
    driver.find_element_by_xpath("//a[contains(@href, 'doc=catalog&category_id=1')]").click()
    goods_number = len(driver.find_elements_by_xpath("//a[contains(@href, 'edit_product&category_id')][count(*)=0]"))
    for n in range(0, goods_number):
        driver.find_elements_by_xpath("//a[contains(@href, 'edit_product&category_id')][count(*)=0]")[n].click()
        driver.back()
    for log in driver.get_log("browser"):
        print(log)
