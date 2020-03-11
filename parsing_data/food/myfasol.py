import requests
import pandas as pd
from pandas import ExcelWriter
import datetime
import re
import json

def get_data():
    all_shop = []
    r = requests.get("https://myfasol.ru/stores/").text
    result = re.findall(r"shops:(.*),", r)[0]
    for shop in json.loads(result):
        print(shop)
        coords = shop['coords'].split(',')
        y, x = coords[0], coords[1]
        store_dict = {
            'address': shop['address'].strip(),
            'working_time': f"{shop['timeOn']} - {shop['timeOff']}",
            'phone': shop['phone'],
            'x': x,
            'y': y,
            'brand_name': 'Фасоль',
            'holding_name': 'METRO Cash&Carry',
            'website': 'https://myfasol.ru/stores/',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)

    return all_shop

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def myfasol_pd_data():
    """
    1. Заходим на страницу https://myfasol.ru/stores/
    2. С помошью рег. выражений находим фрагмент re.findall(r"shops:(.*),", r)[0]
    3. Преобразуем найденый фрагмент в коректный JSON
    4. Перебираем записывыаем в all_shop = [] возврашвем в функцию myfasol_pd_data()
    5. из good_data формируем DF
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'myfasol')
    return df