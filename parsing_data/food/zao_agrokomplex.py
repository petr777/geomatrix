import requests
import pandas as pd
from pandas import ExcelWriter
import datetime


def get_data():
    all_shop = []
    url = 'https://www.zao-agrokomplex.ru/local/ajax/shops.php?type=json'
    # ЧТО ТО РУГАЕТСЯ НА SLL ВЫКЛЮЧАЕМ
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url,  verify=False).json()
    points = r['features']
    for point in points:
        coords = point['geometry']['coordinates']
        y, x = coords[0], coords[1]

        store_dict = {
            'address': point['properties']['Title'],
            'rilos_format': point['properties']['Pay'],
            'working_time': point['properties']['Work'],
            'x': x,
            'y': y,
            'brand_name': 'AgroKompleks',
            'holding_name': 'AgroKompleks',
            'website': 'https://www.zao-agrokomplex.ru',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)
    return all_shop

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def agro_kompleks_pd_data():
    """
    1. Данные по отдаются по ссылке https://www.zao-agrokomplex.ru/local/ajax/shops.php?type=json
    2. Разбираем JSON записываем точки в all_shop
    3. Возвращаем all_shop в функцию agro_kompleks_pd_data в переменную good_data
    4. из good_data формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    #write_xlsx(df, 'AgroKompleks')
    return df



