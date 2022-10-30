"""
1 получить список УРЛов
2 пройтись по нему в цикле

https://inshi.by/katalog/remmers

https://inshi.by/katalog/instrument
"""

import requests
from bs4 import BeautifulSoup
import openpyxl
import json

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
    'https://inshi.by/katalog/remmers',
    'https://inshi.by/katalog/instrument/',
]

prefix = 'https://inshi.by/'

field_names = [
    'name',
    'description',
    'media',
    'technical_description',
    'url',
]


def get_products_list(urls_list: list) -> list:
    products_list = []
    for item in urls_list:
        response = requests.get(item)
        soup = BeautifulSoup(response.text, 'lxml')
        products_list += soup.find_all('span', class_='prod-title')
    return products_list


def clear_products_list(products_list: list):
    cleared_list = []
    for item in products_list:
        if item.text in exceptions_list:
            continue
        cleared_list.append(item)
    return cleared_list


def get_product(products_list, url_prefix=''):
    products = []
    i = 0
    for item in products_list:
        product = {}
        item = url_prefix + item.find('a').get('href')
        response = requests.get(item)
        if response.text == 'Illegal value of &amp;documents: BS2000':
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        product['name'] = soup.find('h1').text
        print(product['name'])
        product['description'] = ''
        descriptions = soup.find('div', class_="sin-product-add-cart")
        descriptions = descriptions.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_siblings
        for description in descriptions:
            if description.name == 'hr':
                break
            product['description'] += description.text.replace('\r', '').replace('\n', '').replace('\t', '') + '\n'
        product['description'] = product['description'].replace('\n\n', '\n')
        medias = soup.find_all('a', class_="fancybox")
        product['media'] = []
        for media in medias:
            product['media'].append(prefix + media.get('href'))
        technical_description = soup.find('div', class_="prod-desc js-product").find('a', target="_blank")
        if technical_description:
            product['technical_description'] = prefix + technical_description.get('href')
        product['url'] = item
        # print(product)
        products.append(product)
        i += 1
        # if i > 10:
        #     print(products)
        #     break
    return products


def save_to_excel(products):
    with open('products.json', 'w') as fp:
        json.dump(products, fp)
    # создаем новый excel-файл
    wb = openpyxl.Workbook()
    # добавляем новый лист
    wb.create_sheet(title='Первый лист', index=0)
    # получаем лист, с которым будем работать
    sheet = wb['Первый лист']
    sheet.append(field_names)
    row = 2
    for item in products:
        col = 1
        print(item['name'])
        for key, value in item.items():
            cell = sheet.cell(row=row, column=col)
            # print(value)
            if isinstance(value, list):
                value = '\n'.join(value)
            cell.value = value
            col += 1
        row += 1
    wb.save('product.xlsx')


def load_json():
    with open('products.json', 'r') as fp:
        products = json.load(fp)
    return products


def main():
    products_list = get_products_list(urls_list)
    products_list = clear_products_list(products_list)
    products = get_product(products_list, url_prefix=prefix)
    save_to_excel(products)


if __name__ == '__main__':
    # main()
    # products = load_json()
    # save_to_excel(products)
