import re
import json
import requests
import pandas as pd
from pandas import ExcelWriter
import datetime

def get_data():
    all_shop = []
    r = requests.get('https://yandex.ru/map-widget/v1/?um=constructor%3A15d2d10dd4fd8c2e32f0b2b7c1f5429222bcc42b7637593686d661bbd97769e8&source=constructor').text
    result = re.findall(r'provide\({"ymj":"1.0"(.*)\);', r)[0]
    JSON = json.loads('{"ymj":"1.0"' + result)

    for items in JSON['maps']:
        for shop in items['geoObjects']['features']:

            coords = shop['geometry']['coordinates']

            x, y = coords[0], coords[1]
            store_dict = {
                'city': shop['properties']['name'],
                'address': shop['properties']['iconCaption'],
                'x': x,
                'y': y,
                'brand_name': 'Хороший выбор',
                'holding_name': 'Хороший выбор',
                'website': 'http://all-rr.ru/Alliance/page10.html',
                'date_review': datetime.datetime.now(),
            }
            all_shop.append(store_dict)
    return all_shop


def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def all_rr_pd_data():
    """
    1. Данные по отдаюия по ссылке https://yandex.ru/map-widget/v1/?um=constructor%3A15d2d10dd4fd8c2e32f0b2b7c1f5429222bcc42b7637593686d661bbd97769e8&source=constructor
    2. С помошью регулярных выражения находим фрагмент с данными
    2. Разбираем JSON записываем точки в all_shop
    3. Возвращаем all_shop в функцию all_rr_pd_data в переменную good_data
    4. из good_data формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    #write_xlsx(df, 'Хороший выбор')
    return df

