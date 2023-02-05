# Перевыпуск бесплатного ssl сертификата
from time import sleep
import requests
from bs4 import BeautifulSoup
import fake_useragent
from pypasser import reCaptchaV3
import asyncio
from pyppeteer import launch
from ssh_user_password import *
import paramiko

url = 'https://punchsalad.com/ssl-certificate-generator/'
url_post = 'https://punchsalad.com/wp-content/themes/oceanwp/ssl-challenge.php'
url_post_1 = 'https://punchsalad.com/wp-content/themes/oceanwp/ssl-file-generator.php'
url_post_2 = 'https://punchsalad.com/wp-content/themes/oceanwp/ssl-selfcheck.php'
url_0 = 'https://punchsalad.com'
user = fake_useragent.UserAgent().random
FILE_PATH = '/home/www/.well-known/acme-challenge/'
checkUrl_prefix = 'http://mx.rizaslovo.ru/.well-known/acme-challenge/'
CERT_FILE_NAME = 'iRedMail.crt'
CERT_PATH = '/etc/ssl/certs/'
KEY_FILE_NAME = 'iRedMail.key'
KEY_PATH = '/etc/ssl/private/'
SSH_COMMAND = 'systemctl restart nginx'


def send_file_to_server(ssh_data, file_name, file_path, ssh_command=''):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ssh_data['server_ip'], ssh_data['port'], username=ssh_data['user'], password=ssh_data['password'],
              timeout=4)
    sftp = s.open_sftp()
    sftp.put(file_name, file_path + file_name)
    if ssh_command:
        s.exec_command(ssh_command)


def save_file(fileName, fileContent):
    with open(fileName, 'w') as file:
        file.write(fileContent)


async def main():
    data = {
        'domainName': 'mx.rizaslovo.ru',
        'emailAddress': 'postmaster@rizaslovo.ru',
        'verificationType': 'http',
        'agreeTos': 'on',
        'recaptcha_response': '',
    }
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': 'example.png'})
    soup = BeautifulSoup(await page.content(), 'lxml')
    ANCHOR_URL = soup.find('div', class_='grecaptcha-badge').div.iframe.get('src')
    recaptcha_response = reCaptchaV3(ANCHOR_URL)
    data['recaptcha_response'] = recaptcha_response
    s = requests.Session()
    response = s.post(url_post, data=data)
    soup = BeautifulSoup(response.text, 'lxml')
    action = url_0 + soup.find('form', class_='dl-challenge').get('action')
    fileName = soup.find('form', class_='dl-challenge').input.get('value')
    fileContent = soup.find('form', class_='dl-challenge').find('input', attrs={'name': 'fileContent'}).get('value')
    data = {
        'fileName': fileName,
        'fileContent': fileContent,
    }
    save_file(fileName, fileContent)
    send_file_to_server(ssh_user_password[0], fileName, FILE_PATH)
    response = s.post(url_post_1, data=data)
    data = {
        'domainName': 'mx.rizaslovo.ru',
        'emailAddress': 'postmaster@rizaslovo.ru',
        'verificationType': 'http',
        'checkUrl': checkUrl_prefix + fileName,
        'verifyRequest': 'true'
    }
    response = s.post(url_post_2, data=data)
    response = s.post(url_post, data=data)
    soup = BeautifulSoup(response.text, 'lxml')
    dlCaBundle = soup.find('form', id='dlCaBundle').textarea.text
    dlPrivateKey = soup.find('form', id='dlPrivateKey').textarea.text
    save_file(CERT_FILE_NAME, dlCaBundle)
    save_file(KEY_FILE_NAME, dlPrivateKey)
    send_file_to_server(ssh_user_password[1], CERT_FILE_NAME, CERT_PATH)
    send_file_to_server(ssh_user_password[1], KEY_FILE_NAME, KEY_PATH, SSH_COMMAND)
    sleep(5)
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
