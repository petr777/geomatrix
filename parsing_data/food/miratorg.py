import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
import json

def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_all_href_city():
    start_page = get_page('https://shop.miratorg.ru/shops/')
    all_city_list = []

    for li in start_page.find('div', class_='header-top-city').find('div', class_='hidden').find_all('li'):
        dict_city = {
            'name': li.text.strip(),
            'url': 'https://shop.miratorg.ru/shops/' + li.find('a')['href']
        }
        all_city_list.append(dict_city)
    return all_city_list

def get_data():
    all_shop = []
    def search_shops(page, city_name):
        stores = re.findall(r'stores: \[(.*)\],', page)[0]
        stores = f'[{stores}]'
        stores = json.loads(stores)
        for store in stores:
            print(store)

            if store['coordinates'] == [0]:
                y, x = None, None
            else:
                y, x = store['coordinates'][0], store['coordinates'][1]

            store_dict = {
                'region': city_name,
                'address': store['address'],
                'working_time': store['open'],
                'rilos_format': store['type'],
                'x': x,
                'y': y,
                'brand_name': 'Miratorg',
                'holding_name': 'Miratorg',
                'website': 'https://shop.miratorg.ru/shops/',
                'date_review': datetime.datetime.now(),
            }
            all_shop.append(store_dict)

    def get_shops_in_city():
        all_city = get_all_href_city()
        for city in all_city:
            print(city['name'])
            # Сессия request назначаем город
            s = requests.Session()
            s.get(city['url'])
            r = s.get('https://shop.miratorg.ru/shops/').text
            search_shops(r, city['name'])
    get_shops_in_city()
    return all_shop


def miratorg_pd_data():
    """
    1. в функции get_all_href_city() средствами bs4 полчаем имена и ссылки по каждому городу
    2. в функции get_shops_in_city() перебираем ссылки с полученнымии городами иницируем ссеию делаем GET запрос
       сначала по ссылке конкретного города, далее GET запрос по url = https://shop.miratorg.ru/shops/
    3. Ответ посылаем в функцию search_shops, где с помошью регулярных выражений ищим фрагмент со всеми магазинами в текушем городе
    4. Найдеый фрагмен переобразуем JSON
    5. Разбираем JSON найденные магазины записываем в all_shop = []
    6. Возвращаем all_shop в функцию miratorg_pd_data в переменную good_data
    5. из good_data формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    #write_xlsx(df, 'miratorg')
    return df

