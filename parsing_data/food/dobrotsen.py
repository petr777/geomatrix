import requests
import pandas as pd
from pandas import ExcelWriter
from bs4 import BeautifulSoup
import datetime
import json
import re


def get_yandex_map_srcipt():
    r = requests.get('http://доброцен.рф/adriesa_maghazinov_')
    page = BeautifulSoup(r.text, 'html.parser')
    yandex_map_srcipt = page.find('div', id='ul-id-129-2').find('script')['src']
    return yandex_map_srcipt

def get_data():
    all_shop = []
    url = get_yandex_map_srcipt()
    r = requests.get(url).text
    result = re.findall(r'"geoObjects":(.*)}],"presetStorage', r)[0]
    JSON = json.loads(result)
    for item in JSON['features']:
        address = item['properties']['name']
        coords = item['geometry']['coordinates']
        print(coords)
        x, y = coords[0], coords[1]

        store_dict = {
            'address': address,
            'x': x,
            'y': y,
            'brand_name': "Dobrotsen",
            'holding_name': "Dobrotsen",
            'website': 'http://доброцен.рф',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)
    return all_shop

def dobrotsen_pd_data():
    """
    1. Заходим на страницу http://доброцен.рф/adriesa_maghazinov_
       на которой средствами BS4  находим ссылку на скрипт отвечаюший за постороение Яндекс карты
    2. Переходим по ссылке с омошью регулярных выражений ищем все точки на карте.
    3. Преобразуем в коректный JSON
    4. Разбирем записываем точки в all_shop
    5. Возврашаем good_data
    6. Формируем DF

    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df


