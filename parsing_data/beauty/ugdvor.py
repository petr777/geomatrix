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


def get_data():
    all_shop = []

    def get_stores_in_city(city, url):
        r = requests.get(url)
        r = r.text.replace('\n', '')
        result = re.findall(r"Placemark\((.*?)}\)\)", r)
        for shop in result:
            coords = re.findall(r'\[(.*)],', shop)[0]
            coords = ast.literal_eval(coords)
            string_data = re.findall(r'<span style="font-size: 12px">(.*)</span>', shop)[0]
            data = BeautifulSoup(string_data, 'lxml')
            data.a.decompose()
            for item in data.find('body').text.split('   '):
                working_time = None
                phone = None
                if 'Адрес:' in item:
                    address = item.replace('Адрес:','')
                    address = address.strip()
                elif 'Время работы:' in item:
                    working_time = item.replace('Адрес:', '')
                    working_time = working_time.strip()
                elif 'Телефон:' in item:
                    phone = item.replace('Телефон: ', '')
                    phone = phone.strip()

                store_dict = {
                    'city': city,
                    'address': address,
                    'working_time': working_time,
                    'phone':phone,
                    'x': coords[1],
                    'y': coords[0],
                    'brand_name': 'Iuzhni Dvor',
                    'holding_name': 'Iuzhni Dvor',
                    'website': 'http://www.ugdvor.ru/',
                    'date_review': datetime.datetime.now(),
                }
                print(store_dict)
                all_shop.append(store_dict)


    def get_all_city():
        start_page = get_page('https://www.ugdvor.ru/map/')
        for map in start_page.find('div', class_='items').find_all('div', class_="map-item"):
            city_url  = 'https://www.ugdvor.ru' + map.a['href']
            name_city =  map.a.text.strip()
            get_stores_in_city(name_city, city_url)

    get_all_city()
    return all_shop

def ugdvor_pd_data():
    """
    1. в функции get_all_city() находим ссылки на все города и их наименование
    2. Циклом перебираем и отправлекм найденное в функцию get_stores_in_city()
    3. С помошью регулярноговыражения находим все фрагменты с данными по магазинам в текушем городе
       --- result = re.findall(r"Placemark\((.*?)}\)\)", r) ---
    4. Циклом перебираем найденное с помошью регулярок
         4.1 опять же с помошью регулярных выражений находим координаты
            -- coords = re.findall(r'\[(.*)],', shop)[0] ---
         4.2 и фрагмент с данными по конкретному магазину
         --- string_data = re.findall(r'<span style="font-size: 12px">(.*)</span>', shop)[0]---
         далее с помошью манапуляций с текстом разбираем найдженный фрагмент

         4.3 Записываем кореектные данные в all_shop = []
    5. Возврашаем  all_shop = [] в ugdvor_pd_data()
    6. Где формируем df
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df

