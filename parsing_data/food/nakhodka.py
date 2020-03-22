import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
import json


def get_yandex_map_url():
    r = requests.get('https://nahodka-magazin.ru/magaziny/')
    page = BeautifulSoup(r.text, 'html.parser')
    map = page.find('div', class_='this_map').iframe['src']
    return map

def get_point():
    all_shop = []
    url_yandex_map_url = get_yandex_map_url()
    r = requests.get(url_yandex_map_url).text
    stores_data_row = re.findall(r'provide\({"ymj":"1.0","maps":(.*),"presetStorage"', r)[0]
    JSON = json.loads(stores_data_row)
    points = [point['geoObjects']['features'] for point in JSON]
    for point in points[0]:
        address = point['properties']['name']
        coords = point['geometry']['coordinates']
        # Исключение
        if 'г.Октябрьский' in address:
            address = 'Россия, Республика Башкортостан, ' + address
        x, y = coords[0], coords[1]
        store_dict = {
            'address': address,
            'x': x,
            'y': y,
            'brand_name': 'Nakhodka',
            'holding_name': 'Nakhodka',
            'website': 'https://nahodka-magazin.ru/magaziny/',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)
    return all_shop

def nakhodka_pd_data():
    """
    1. Отправляем запрос https://nahodka-magazin.ru/magaziny/ средствами bs4 аходим ссылку на frame с яндекс картами
    2. Переходим по найденной ссылке с помошью регулярного выражения находим точки на карте.
       (stores_data_row = re.findall(r'provide\({"ymj":"1.0","maps":(.*),"presetStorage"', r)[0])
    3. Преобразуем найденное в dict
     5. Формируем store_dict который записываем в all_shop = []
    7. Возврашаем all_shop = [] в функцию nakhodka_pd_data(), где формируем DF
    """
    good_data = get_point()
    df = pd.DataFrame(good_data)
    return df
