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


def get_spec(url, driver):
    spec = {}
    response = requests.get(url, cookies=driver.get_cookies())
    # response = driver.execute_script(f'''
    #     var xmlHttp = new XMLHttpRequest();
    #     xmlHttp.open( "GET", "{url}", false );
    #     xmlHttp.send( null );
    #     return xmlHttp.responseText;
    # '''
    #                                  )
    # soup = BeautifulSoup(response.text, 'lxml')
    soup = BeautifulSoup(response.text, 'lxml')
    spec['deadline'] = soup.find('span', string='Срок сдачи')
    print(soup)


# def popup_close(driver):
#     try:
#         element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)


def main():
    s = requests.Session()
    driver = webdriver.Chrome()
    main_captcha(driver)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup)
    # sleep(30)
    while True:
        for item in soup.find_all('div', class_='SiteSnippetSearch SitesSerp__snippet'):
            url = PREFIX + item.a.get('href')
            print(url)
            get_spec(url, driver)
        break

    #     'https://realty.ya.ru/moskva_i_moskovskaya_oblast/kupit/novostrojka/?showOutdated=NO&page=48'
    # print(driver.page_source)


# async def main2():
#     browser = await launch()
#     # page = await browser.newPage()
#     # await page.goto('https://example.com')
#     # await page.screenshot({'path': 'example.png'})
#     sleep(30)
#     await browser.close()


if __name__ == '__main__':
    main()
    # asyncio.get_event_loop().run_until_complete(main2())
