import re
from selenium import webdriver
from _pytest.fixtures import fixture
from selenium.webdriver.chrome.options import Options


def check_grey(color):
    codes_list = color.split(", ")
    first_code = re.sub('\D', '', codes_list[0])
    second_code = codes_list[1]
    if first_code != second_code:
        raise AssertionError("The color is not grey.")


def check_red(color):
    codes_list = color.split(", ")
    first_code = codes_list[1]
    second_code = first_code = re.sub('\D', '', codes_list[2])
    if first_code != "0":
        raise AssertionError("The color is not red.")
    elif second_code != "0":
        raise AssertionError("The color is not red.")


def check_1st_size_bigger_than_2nd(first_size, second_size):
    first_area = first_size['height'] * first_size['width']
    second_area = second_size['height'] * second_size['width']
    if first_area <= second_area:
        raise AssertionError("1st size is not bigger.")


@fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    wd = webdriver.Chrome(options=chrome_options)
    # wd = webdriver.Ie()
    # wd = webdriver.Firefox(firefox_binary="c:\\Program Files\\Mozilla Firefox\\firefox.exe")
    wd.implicitly_wait(10)
    yield wd
    wd.quit()


def test_correct_values_of_products(driver):
    driver.get("http://localhost/litecart/")
    first_campaigns_product = driver.find_element_by_xpath("//*[@id='box-campaigns']//a[@class='link'][1]")
    main_page_product_title = first_campaigns_product.find_element_by_xpath(".//*[@class='name']").get_attribute("textContent")
    # next locator checks strikethrough because of .//s (point в)
    main_page_regular_price = first_campaigns_product.find_element_by_xpath(".//s[@class='regular-price']")
    main_page_regular_price_color = main_page_regular_price.value_of_css_property("color")
    check_grey(main_page_regular_price_color)  # point в
    main_page_regular_price_value = main_page_regular_price.get_attribute("textContent")
    # next locator checks bold because of .//strong (point г)
    main_page_campaign_price = first_campaigns_product.find_element_by_xpath(".//strong[@class='campaign-price']")
    main_page_campaign_price_color = main_page_campaign_price.value_of_css_property("color")
    check_red(main_page_campaign_price_color)  # point г
    main_page_campaign_price_value = main_page_campaign_price.get_attribute("textContent")
    check_1st_size_bigger_than_2nd(main_page_campaign_price.size, main_page_regular_price.size)  # point д

    driver.get(first_campaigns_product.get_attribute("href"))
    good_page_product_title = driver.find_element_by_xpath("//*[@itemprop='name']").get_attribute("textContent")
    if main_page_product_title != good_page_product_title:  # point а
        raise AssertionError("Titles don't match.")
    # next locator checks strikethrough because of .//s (point в)
    good_page_regular_price = driver.find_element_by_xpath("//s[@class='regular-price']")
    good_page_regular_price_color = good_page_regular_price.value_of_css_property("color")
    check_grey(good_page_regular_price_color)  # point в
    good_page_regular_price_value = good_page_regular_price.get_attribute("textContent")
    if main_page_regular_price_value != good_page_regular_price_value:  # point б
        raise AssertionError("Regular prices don't match.")
    # next locator checks bold because of .//strong (point г)
    good_page_campaign_price = driver.find_element_by_xpath("//strong[@class='campaign-price']")
    good_page_campaign_price_color = good_page_campaign_price.value_of_css_property("color")
    check_red(good_page_campaign_price_color)  # point г
    good_page_campaign_price_value = good_page_campaign_price.get_attribute("textContent")
    if main_page_campaign_price_value != good_page_campaign_price_value:  # point б
        raise AssertionError("Campaign prices don't match.")
    check_1st_size_bigger_than_2nd(good_page_campaign_price.size, good_page_regular_price.size)  # point д
