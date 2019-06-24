# -*- coding: utf-8 -*-
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-extensions")
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("headless")
    # options.add_argument("–disable-dev-shm-usage")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--test-type")
    options.add_argument('disable-infobars')
    options.binary_location = "/usr/bin/chromium-browser"
    chrome_driver_binary = "/usr/local/bin/chromedriver"
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    wd = webdriver.Chrome(chrome_driver_binary, options=options, service_args=["--verbose", "--log-path=/tmp/chromedriverxx.log"], desired_capabilities=d)
    request.addfinalizer(wd.quit)
    return wd


site = 'https://domain.com/'


def get_hrefs(links):
    hrefs = list()
    for link in links:
        try:
            href = link.get_attribute('href')
            if 'domain' in href:
                hrefs.append(href)
        except Exception:
            continue
    return list(set(hrefs))


def test_ex(driver):
    driver.get(site)
    href_list = get_hrefs(driver.find_elements_by_xpath("//a"))
    total = list()
    for href in href_list:
        try:
            driver.get(href)
            child = get_hrefs(driver.find_elements_by_xpath("//a"))
            total += child
        except Exception:
            continue
    total = set(total + href_list)
    for link in total:
        r = requests.head(link)
        if r.status_code > 400:
            print('Cannot get to', link)
        else:
            print(link, 'OK')
