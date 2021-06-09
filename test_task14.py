from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def test_windows(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    driver.find_element_by_xpath("//a[contains(@href, 'countries')]").click()
    driver.find_element_by_xpath("//a[@class='button']").click()
    link_icons = driver.find_elements_by_xpath("//form//a[@target='_blank']")
    for link_icon in link_icons:
        handles = driver.window_handles
        link_icon.click()
        wait = WebDriverWait(driver, 3)
        wait.until(EC.new_window_is_opened(handles))
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
