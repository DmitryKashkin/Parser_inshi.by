"""
1 получить список УРЛов
2 пройтись по нему в цикле

https://inshi.by/katalog/remmers

https://inshi.by/katalog/instrument
"""

import requests
from bs4 import BeautifulSoup
import openpyxl

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


def get_product(products_list, url_prefix=''):
    product = {}
    products = []
    for item in products_list:
        item = url_prefix + item.find('a').get('href')
        response = requests.get(item)
        soup = BeautifulSoup(response.text, 'lxml')
        product['name'] = soup.find('h1').text
        product['description'] = ''
        descriptions = soup.find('div', class_="prod-desc js-product").find_all('p')
        for description in descriptions:
            product['description'] += description.text.replace('\r', '').replace('\n', '').replace('\t', '') + '\n'
        medias = soup.find_all('a', class_="fancybox")
        product['media'] = []
        for media in medias:
            product['media'] += media.get('href')
        product['technical_description'] = soup.find('div', class_="prod-desc js-product").find('a',
                                                                                                target="_blank").get(
            'href')
        print(product)
        products += product
        break
    return products


def save_to_excel(products):
    # создаем новый excel-файл
    wb = openpyxl.Workbook()
    # добавляем новый лист
    wb.create_sheet(title='Первый лист', index=0)
    # получаем лист, с которым будем работать
    sheet = wb['Первый лист']
    for row in range(1, 4):
        for col in range(1, 4):
            value = str(row) + str(col)
            cell = sheet.cell(row=row, column=col)
            cell.value = value
    wb.save('product.xlsx')


def main():
    products_list = get_products_list(urls_list)
    products_list = clear_products_list(products_list)
    products = get_product(products_list, url_prefix=prefix)


if __name__ == '__main__':
    # main()
    # product = {}
    # item = 'https://inshi.by/katalog/remmers/zashhita-drevesiny/antiseptiki/aqua-ig-15-impagniergrund-it'
    # response = requests.get(item)
    # soup = BeautifulSoup(response.text, 'lxml')
    # product['name'] = soup.find('h1').text
    # product['description'] = ''
    # descriptions = soup.find('div', class_="prod-desc js-product").find_all('p')
    # for description in descriptions:
    #     product['description'] += description.text.replace('\r', '').replace('\n', '').replace('\t', '') + '\n'
    # print(product)
    save_to_excel('test')