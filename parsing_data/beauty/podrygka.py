import requests
from bs4 import BeautifulSoup
import re
import ast
import datetime
import pandas as pd
from pandas import ExcelWriter


def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_dop_data(html):
    fragment = BeautifulSoup(html, 'lxml')
    store_field = fragment.find('div', class_='store-field')
    working_time = store_field.find('div', class_="schedule store-field").find('span').text
    working_time = working_time.replace('\t','')
    # Забираем превую строчку
    address = store_field.find_all('span')[0].text.split('\n')[0]
    return address, working_time


def get_data():
    all_shop = []
    def get_stores_in_city(url):
        page = get_page(url).prettify()
        result = re.findall(r'var stores = \[(.*?)];', page)[0]
        result = '[' + result + ']'
        for store in ast.literal_eval(result):
            address, working_time = get_dop_data(store['BALLOON']['HTML'])
            store_dict = {
                    'address': address,
                    'working_time': working_time,
                    'x': store['PLACEMARK']['COORDINATES'][1],
                    'y': store['PLACEMARK']['COORDINATES'][0],
                    'brand_name': 'Podruzhka',
                    'holding_name': "L'Etoile",
                    'website': 'https://www.podrygka.ru',
                    'date_review': datetime.datetime.now(),
                }
            all_shop.append(store_dict)

    def get_all_city_url():
        # Ищем все города где есть магазины
        page = get_page('https://www.podrygka.ru/shoplist/')
        all_city_url = page.find('select', class_='js-select waiting-for-style').find_all('option')
        # Приводим найденое к коректому url
        all_city_url = [x['data-control_id'] for x in all_city_url]
        all_city_url = [x.split('_') for x in all_city_url]
        for url in all_city_url:
            url = f'https://www.podrygka.ru/shoplist/?{url[0]}_{url[1]}={url[2]}&set_filter=y'
            print(url)
            get_stores_in_city(url)
    get_all_city_url()
    return all_shop



def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def podrygka_pd_data():
    """
    1. в функции def get_all_city_url() средстави bs4 получаем список параметров для формирования коректного url
        пример: https://www.podrygka.ru/shoplist/?arrShopsSmartFilter_68=498629140&set_filter=y

    2. Циклом перебираем полученные url
    3. На странице с помошью рег. выражений находим фрагмент со всеми магазинами в текушем городе
       result = re.findall(r'var stores = \[(.*?)];', page)[0]
       3.1 Забираем координаты
       3.2 Отправляем фрагмент HTML в функцию get_dop_data()
            - Средствами bs4 и манипуляций с текстом получаем время работы и адрес которые возврашаем в функцию get_stores_in_city
    4. Записываем все магазины в all_shop = []
    5. Который возврашаем в функцию podrygka_pd_data()
    6. формируем df

    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    #write_xlsx(df, 'podrygka')
    return df

