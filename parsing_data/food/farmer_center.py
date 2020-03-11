import requests
import pandas as pd
from pandas import ExcelWriter
import datetime
import re


def get_data():
    all_shop = []
    url = "https://фермер-центр.рф/stores/"
    r = requests.get(url).text
    # ВРЕМЯ РАБОТЫ ОДНО ДЛЯ ВСЕХ
    time_work = re.findall(r"let rr = '<br/>(.*)';", r)[0]
    for row in re.findall(r"DG.marker\((.*);", r):
        # Делаем строки одинаковыми убираем иконки шариков это магазины недавно открывшиеся
        row = row.replace(', {icon: i2}', '')
        # Ставим всесто фрагмента текста ","
        row = row.replace(").addTo(map).bindPopup('", ',')
        # И убиираем ненужное окончание
        row = row.replace("'+rr)", '')
        # Забираем из строки координаты
        coord = re.findall(r"\[(.*)]", row)[0]
        y, x = coord.split(',')
        # Удаляем координаты из строки оставляем только адрес
        address = re.sub(r"\[(.*)],",'',row)
        # Время работы
        status = 'Open'

        # Это иконка строительного крана если она есть то магазин скоро откроется
        if ' {icon: i1},' in address:
            status = "opening soon"
            address = address.replace(' {icon: i1},', '')

        store_dict = {
            'address': address,
            'working_time': time_work,
            'status': status,
            'x': x,
            'y': y,
            'brand_name': 'Fermer Tsentr RF',
            'holding_name': 'Fermer Tsentr RF',
            'website': 'https://фермер-центр.рф/stores/',
            'date_review': datetime.datetime.now(),

        }
        all_shop.append(store_dict)

    return all_shop


def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'


def fermer_tsentr_pd_data():
    """
    1. отпарвляем запрос к странице "https://фермер-центр.рф/stores/"
    2. В ответ ищем все точки re.findall(r"DG.marker\((.*);", r) наннесенные на карту 2GIS
    3. Разбираем с помошью реулярных выражений СМ. САМУ ФУНКЦИЮ постораля документировать каждое действие
    4. Записывам точки all_shop = []
    5. Возвращаем all_shop в функцию fermer_tsentr_pd_data в переменную good_data
    6. из good_data формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    #write_xlsx(df, 'Fermer_Tsentr')
    return df






