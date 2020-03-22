import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
import json
from urllib.parse import urlparse

def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_coords_and_city(url, address):
    page = get_page(url)
    # Находим  сслыку с координатами
    html = page.find('a', class_="address")
    href = html['href']

    # Приводим к коректому формату
    result = re.findall(r'pt=(.*)', href)[0]
    result = result.replace('E', '')
    result = result.replace('N', '')
    coords = result.split(',')

    # Для получения имени города убираем адресс из строки
    name_city = html.text
    name_city = name_city.replace(f', {address}', '')

    return coords, name_city


def get_all_store():
    all_shop = []
    url = 'https://baucenter.ru/store/'
    page = get_page(url)
    all_shop_fragment_html = page.find('div', class_='catalog-right advices-padding').find_all('section')

    for shop in all_shop_fragment_html:
        href = shop.find('div', class_='advice_item').a['href']
        detail_url = 'https://baucenter.ru' + href

        address = shop.find('div', class_='advice_item').a.h3.text
        address = address.replace('ТЦ на', '')

        coords, name_city = get_coords_and_city(detail_url, address)

        working_time = shop.find_all('p')[0].text
        working_time = working_time.replace('Часы работы: ', '')

        phone = shop.find_all('p')[1].text
        phone = phone.replace('Телефон:', '')

        store_dict = {
            'city': name_city,
            'address': address,
            'working_time': working_time,
            'phone': phone,
            'x': coords[0],
            'y': coords[1],
            'brand_name': 'Bautsentr',
            'holding_name': 'Bautsentr',
            'website': 'https://baucenter.ru/store/',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)

    return all_shop


def bautsentr_pd_data():
    """
    1. Отправляем запрос https://baucenter.ru/store/
    2. Средствами bs4 находим все магазины
       all_shop_fragment_html = page.find('div', class_='catalog-right advices-padding').find_all('section')
    3. Перебираем циклом и с помошью bs4 забираем часть данных, также находим ссылку на детальное описание магазина
    4. отпраляем ее и адрес в функцию get_coords_and_city(), где с помощью bs4 находим координаты
       (координаты хранятся в ссылке на yandex карты ) СМ. Функцию описание внутри
    5. Формируем store_dict который записываем в all_shop = []
    7. Возврашаем all_shop = [] в функцию bautsentr_pd_data(), где формируем DF

    """
    good_data = get_all_store()
    df = pd.DataFrame(good_data)
    return df

