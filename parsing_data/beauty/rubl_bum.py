import requests
import pandas as pd
from pandas import ExcelWriter
import datetime
import re
import json

def get_data():
    all_shop = []
    r = requests.get('http://1b.ru/pokupatelyam/o-magazinax')
    points = re.findall(r'"ShopsList":\[(.*)\],', r.text)[0]
    points = f'[{points}]'
    points = json.loads(points)
    for point in points:
        print(point)
        store_dict = {
            'region': point['region'].strip(),
            'rilos_format': point['type'],
            'x': point['lng'],
            'y': point['lat'],
            'brand_name': 'Rubl Bum',
            'holding_name': 'Rubl Bum',
            'website': 'http://1b.ru',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)
    return all_shop


def rubl_bum_pd_data():
    # TODO сомительная точность координат ПРОВЕРИТЬ
    """
    1. Запрос к странице http://1b.ru/pokupatelyam/o-magazinax
    2. С помошью регулярных выражений находим фрагмент "ShopsList":
    3. Преобразуем фрагмент в коректный json
    4. Разбираем json записываем точки в all_shop = []
    5. Возврашаем all_shop в функцию rubl_bum_pd_data
    6. Формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df

