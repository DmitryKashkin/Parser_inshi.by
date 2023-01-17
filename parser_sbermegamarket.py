import requests
from bs4 import BeautifulSoup
import openpyxl
import json
from slugify import slugify
import platform
from selenium import webdriver

if platform.system() == 'Windows':
    PHANTOMJS_PATH = './phantomjs.exe'
else:
    PHANTOMJS_PATH = './phantomjs'

URL = 'https://sbermegamarket.ru/catalog'


def get_content_2(url):
    browser = webdriver.PhantomJS(PHANTOMJS_PATH)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, "lxml")
    print(soup)


def get_content(url):
    response = requests.get(url)
    # print(response.text)
    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)
    for item in soup.find_all('div', class_='catalog-category-cell catalog-department__category-item'):
        url2 = item.find('a').get('href')
        print(url2)


def main():
    get_content_2(URL)


if __name__ == '__main__':
    main()
