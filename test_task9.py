from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options


@fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    wd = webdriver.Chrome(options=chrome_options)
    wd.implicitly_wait(10)
    yield wd
    wd.quit()


def test_countries_and_zones(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    # check countries alphabetical order
    countries = driver.find_elements_by_xpath("//form[@name='countries_form']//tr[@class='row']/td[5]/a")
    countries_list = []
    for country in countries:
        countries_list.append(country.get_attribute("textContent"))
    if sorted(countries_list) != countries_list:
        raise AssertionError("Countries are not in alphabetical order.")
    # check zones
    zones = driver.find_elements_by_xpath("//form[@name='countries_form']//tr[@class='row']/td[6]")
    country_link_not_zero_zone = []
    for zone in zones:
        if zone.get_attribute("textContent") != '0':
            country_link_not_zero_zone.append(zone.find_element_by_xpath(".//preceding::td[1]/a").get_attribute("href"))
    for n in range(0, len(country_link_not_zero_zone)):
        driver.get(country_link_not_zero_zone[n])
        zones = driver.find_elements_by_xpath("//*[@id='table-zones']//td[3]//*[@name!='zone[name]']//parent::td")
        zones_list = []
        for zone in zones:
            zones_list.append(zone.get_attribute("textContent"))
        if sorted(zones_list) != zones_list:
            raise AssertionError("Zones are not in alphabetical order.")


def test_geo_zones(driver):
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("admin")
    driver.find_element_by_xpath("//button[@name='login']").click()
    names = driver.find_elements_by_xpath("//form[@name='geo_zones_form']//tr[@class='row']/td[3]/a")
    country_links = []
    for name in names:
        country_links.append(name.get_attribute("href"))
    for n in range(0, len(country_links)):
        driver.get(country_links[n])
        selected_zones = driver.find_elements_by_xpath("//table[@id='table-zones']//td[3]//option[@selected]")
        zones_list = []
        for zone in selected_zones:
            zones_list.append(zone.get_attribute("textContent"))
        if sorted(zones_list) != zones_list:
            raise AssertionError("Zones are not in alphabetical order.")