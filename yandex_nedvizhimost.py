import asyncio
import os
from time import sleep
from selenium import webdriver
import selenium
import requests
from bs4 import BeautifulSoup
import openpyxl
import json
# from slugify import slugify
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyppeteer import launch
import pickle

URL = 'https://realty.ya.ru/moskva_i_moskovskaya_oblast/kupit/novostrojka/?showOutdated=NO'
URL2 = 'https://dzen.ru/?yredirect=true'
CSS_CAPTCHA = '#root > div > div > form > div.Spacer.Spacer_auto-gap_bottom > div > div > div.CheckboxCaptcha-Anchor > input'
PREFIX = 'https://realty.ya.ru'


def main_captcha(driver):
    driver.get(URL)
    try:
        for cookie in pickle.load(open('ya_cookies', 'rb')):
            driver.add_cookie(cookie)
    except FileNotFoundError:
        try:
            element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)
        except:
            return
        driver.execute_script("arguments[0].click();", element)
        sleep(3)
        pickle.dump(driver.get_cookies(), open('ya_cookies', 'wb'))
    else:
        driver.get(URL)
    sleep(3)


def get_spec(url, s):
    spec = {}
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    spec['deadline'] = soup.find('span', string='Срок сдачи').next_sibling.text.replace('\xa0',' ')
    spec['class'] = soup.find('span', string='Класс жилья').next_sibling.a.text.replace('\xa0',' ')
    print(spec)


# def popup_close(driver):
#     try:
#         element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)


def main():
    s = requests.Session()
    # resp=s.get(URL)
    # print(resp.text)
    driver = webdriver.Chrome()
    main_captcha(driver)
    [s.cookies.set(c['name'], c['value']) for c in driver.get_cookies()]
    soup = BeautifulSoup(driver.page_source, 'lxml')
    while True:
        for item in soup.find_all('div', class_='SiteSnippetSearch SitesSerp__snippet'):
            url = PREFIX + item.a.get('href')
            print(url)
            get_spec(url, s)
        break





if __name__ == '__main__':
    main()
