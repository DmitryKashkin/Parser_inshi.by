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
PAGE = 'https://realty.ya.ru/moskva_i_moskovskaya_oblast/kupit/novostrojka/?showOutdated=NO&page='
URL2 = 'https://dzen.ru/?yredirect=true'
CSS_CAPTCHA = '#root > div > div > form > div.Spacer.Spacer_auto-gap_bottom > div > div > div.CheckboxCaptcha-Anchor > input'
PREFIX = 'https://realty.ya.ru'


# def load_cookie(driver,url):
#     try:
#         for cookie in pickle.load(open('ya_cookies', 'rb')):
#             driver.add_cookie(cookie)
#     except FileNotFoundError:
#         main_captcha(driver,url)
#         pickle.dump(driver.get_cookies(), open('ya_cookies', 'wb'))


def main_captcha(driver, url, s):
    while True:
        driver.delete_all_cookies()
        driver.get(url)
        try:
            element = driver.find_element(By.CSS_SELECTOR, CSS_CAPTCHA)
        except:
            return
        driver.execute_script("arguments[0].click();", element)
        sleep(3)
        s.cookies.clear()
        [s.cookies.set(c['name'], c['value']) for c in driver.get_cookies()]
        response = s.get(url)
        # driver.refresh()
        if 'captcha' in response.text:
            continue
        break
    return response



def get_spec(url, s, driver):
    spec = {}
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        spec['deadline'] = soup.find('span', string='Срок сдачи').next_sibling.text.replace('\xa0', ' ')
    except:
        print('!!!!!!!!!!!!!!!!!!!captcha!!!!!!!!!!!!!!!!!!!')
        response = main_captcha(driver, url, s)
        try:
            soup = BeautifulSoup(response.text, 'lxml')
        except:
            print(response)
            sleep(300)
        spec['deadline'] = soup.find('span', string='Срок сдачи').next_sibling.text.replace('\xa0', ' ')
    spec['class'] = soup.find('span', string='Класс жилья').next_sibling.a.text.replace('\xa0', ' ')
    spec['home_type'] = soup.find('div', string='Тип дома').next_sibling.text.replace('\xa0', ' ')
    spec['buildings'] = soup.find('div', string='Число корпусов').next_sibling.text.replace('\xa0', ' ')
    spec['finish'] = soup.find('h2', string='Ещё параметры').next_sibling.contents[1].contents[1].text.replace('\xa0',
                                                                                                               ' ')
    spec['queues'] = soup.find('div', string='Очереди').next_sibling.text.replace('\xa0', ' ')
    try:
        spec['num_of_apart'] = soup.find('div', string='Число квартир').next_sibling.text.replace('\xa0', ' ')
    except:
        spec['num_of_apart'] = soup.find('div', string='Число квартир и апартаментов').next_sibling.text.replace('\xa0', ' ')


        # print(soup)
        # print('')
        # print(url)
        # with open('products.json', 'w') as fp:
        #     json.dump(str(soup), fp)
        # sleep(100)




def main():
    s = requests.Session()
    driver = webdriver.Chrome()
    response = main_captcha(driver, URL, s)
    # [s.cookies.set(c['name'], c['value']) for c in driver.get_cookies()]
    soup = BeautifulSoup(response.text, 'lxml')
    page_number = 1
    while True:
        print('!!!!!page_number ', page_number)
        for item in soup.find_all('div', class_='SiteSnippetSearch SitesSerp__snippet'):
            url = PREFIX + item.a.get('href')
            print(url)
            get_spec(url, s, driver)
        page_number += 1
        response = s.get(PAGE + str(page_number))
        if '404' in response:
            break


if __name__ == '__main__':
    main()
