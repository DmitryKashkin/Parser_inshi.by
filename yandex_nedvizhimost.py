import os
from time import sleep
from selenium import webdriver
import selenium
import requests
from bs4 import BeautifulSoup
import openpyxl
import json
from slugify import slugify
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://realty.ya.ru/moskva_i_moskovskaya_oblast/kupit/novostrojka/?showOutdated=NO'
CSS_CAPTCHA = '#root > div > div > form > div.Spacer.Spacer_auto-gap_bottom > div > div > div.CheckboxCaptcha-Anchor > input'


def main_captcha(driver):
    try:
        element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)
    except:
        return
    driver.execute_script("arguments[0].click();", element)
    sleep(1)


# def popup_close(driver):
#     try:
#         element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)


def main():
    # response = requests.get(URL)
    # print(response.text)
    driver = webdriver.Chrome()
    driver.get(URL)
    main_captcha(driver)


    print(driver.page_source)


if __name__ == '__main__':
    main()
