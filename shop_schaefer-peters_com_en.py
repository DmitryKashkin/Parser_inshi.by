from time import sleep
import requests
from bs4 import BeautifulSoup

item_list = []
SUFFIX = '?pgNr='
URL = 'https://shop.schaefer-peters.com/en/'


def get_item(cat_list, s):
    for url in cat_list:
        suffix = ''
        page = 0
        while True:
            response = s.get(url + suffix)
            if response.url != url + suffix:
                break
            soup = BeautifulSoup(response.text, 'lxml')
            tbody = soup.find('div', class_='list-container')
            for item in tbody.find_all('tr', class_='sp-product-item'):
                print(item.find('a').get('href'))
                item_list.append(get_spec(item.find('a').get('href'), s))
            page += 1
            suffix = SUFFIX + str(page)


def get_spec(url, s):
    item_spec = {
        'art': ' ',
        'art2': ' ',
        'cat_path': ' ',
        'url': ' ',
        'img_urls': ' ',
    }
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    item_spec['cat_path'] = soup.find('div', id='breadcrumb').text
    item_spec['url'] = url
    content_box = soup.find('div', class_='content-box')
    art = content_box.find('div', class_='col-xs-12 attribute-title')
    item_spec['art'] = art.h1.text
    item_spec['art2'] = art.span.text
    img_urls = content_box.find('div', class_='details-image-gallery')
    item_spec['img_urls'] = ', '.join(
        [i.get('data-src') for i in img_urls.find_all('div', class_='item') if i.get('data-src')])
    custom_attributes = content_box.find('div', class_='custom-attributes').find_all('div', class_='row')
    for attrib in custom_attributes:
        if attrib.div.span.strong:
            key = attrib.contents[1].text.replace('\n', '')
            value = attrib.contents[3].text.replace('\n', '').replace(' ', '')
            item_spec[key] = value
    relatedInfo_relatedInfoFull = content_box.find('div', class_='tab-content')
    for attrib in relatedInfo_relatedInfoFull.find_all('div', class_='row'):
        key = attrib.contents[1].text.replace('\n', '')
        value = attrib.contents[3].text.replace('\n', '').replace(' ', '')
        item_spec[key] = value
    item_spec['application_area'] = relatedInfo_relatedInfoFull.find('div', class_="tab-pane", id='tab4').text.replace(
        '\n', '')
    catalogue_pages = relatedInfo_relatedInfoFull.find('a', class_='sx-product-download').get('data-filename')
    item_spec['catalogue_pages'] = url + catalogue_pages
    url0 = 'https://shop.schaefer-peters.com/index.php?lang=1&#'
    form_data = {'target': "_blank",
                 'class': "sx-product-download",
                 'data-guid': "9e3d3706-f2f8-43a8-9918-25733535b871",
                 'data-filename': "Gesamtkatalog DE-EN  717.pdf"
                 }
    pdf = s.post(url0, data=form_data)

    # pdf = s.get(item_spec['catalogue_pages'])
    sleep(3)


def get_cat(url, s):
    cat_list = []
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for cat_menu in soup.find_all('ul', class_='level-4'):
        cat_list.append(cat_menu.find('a').get('href'))
        # print(cat_menu.find('a').get('href'))
    return cat_list


def main():
    s = requests.Session()
    cat_list = get_cat(URL, s)
    get_item(cat_list, s)


if __name__ == '__main__':
    main()
