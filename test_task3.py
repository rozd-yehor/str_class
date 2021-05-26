import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    wd.maximize_window()
    request.addfinalizer(wd.quit)
    return wd


def test_login_to_admin(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()