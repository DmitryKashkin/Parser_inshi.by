"""
1 получить список УРЛов
2 пройтись по нему в цикле

https://inshi.by/katalog/remmers

https://inshi.by/katalog/instrument
"""

import requests
from bs4 import BeautifulSoup

exceptions_list = [
    'Кисти',
    'STORCH',
    'Инструмент для наливных полов',
    'Оборудование',
    'Крепеж Camo',
    'Строительство и ремонт',
    'Защита древесины',
    'Декоративные и промышленные наливные полы',
    'Защита и ремонт фасадов',
    'Интерьерные краски',
]

urls_list = [
    'https://inshi.by/katalog/instrument/',
    'https://inshi.by/katalog/remmers',
]

prefix = 'https://inshi.by/'


def get_products_list(urls_list: list) -> list:
    products_list = []
    for item in urls_list:
        response = requests.get(item)
        soup = BeautifulSoup(response.text, 'lxml')
        products_list += soup.find_all('span', class_='prod-title')
    return products_list


def clear_products_list(products_list: list):
    cleared_list = []
    # for item in products_list:
    #     if itme in exceptions_list:
    #         continue
    #
    # print(products_list)
    for item in products_list:
        if item.text in exceptions_list:
            continue
        cleared_list.append(item)
    return cleared_list


def main():
    products_list = get_products_list(urls_list)
    products_list = clear_products_list(products_list)

    # response = requests.get('https://inshi.by/katalog/remmers')
    # soup = BeautifulSoup(response.text, 'lxml')
    # products_list = soup.find_all('span', class_='prod-title')

    for item in products_list:
        print(item.find('a').get('href'))
    # print(item.text)
    # print(item)


if __name__ == '__main__':
    main()
