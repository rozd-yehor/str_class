import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    wd.maximize_window()
    request.addfinalizer(wd.quit)
    return wd


def test_open_google(driver):
    driver.get("https://google.com/")