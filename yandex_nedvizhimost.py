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

URL = 'https://realty.ya.ru/moskva_i_moskovskaya_oblast/kupit/novostrojka/?showOutdated=NO'
CSS_CAPTCHA = '#root > div > div > form > div.Spacer.Spacer_auto-gap_bottom > div > div > div.CheckboxCaptcha-Anchor > input'


def main_captcha(driver):
    try:
        element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)
    except:
        return
    driver.execute_script("arguments[0].click();", element)
    sleep(3)


# def popup_close(driver):
#     try:
#         element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)


def main():
    # response = requests.get(URL)
    # print(response.text)
    driver = webdriver.Chrome()
    driver.get(URL)
    main_captcha(driver)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup)
    # sleep(30)
    while True:
        # print('while')
        for item in soup.find_all('div', class_='SiteSnippetSearch SitesSerp__snippet'):
            # print(item)
            print(item.a.get('href'))
            # for item2 in item.find_all('div', class_='Link Link_js_inited Link_size_m Link_theme_islands'):
            #     print(item2.get('href'))
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
