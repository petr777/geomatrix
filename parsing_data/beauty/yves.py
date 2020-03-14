import requests
import re
import json
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from pandas import ExcelWriter

def get_data():
    all_shops = []
    domian = 'http://storelocator.yves-rocher.com'

    def get_data_in_page(url, pattern):
        r = requests.get(url)
        result = re.findall(pattern, r.text)[0] + ']]'
        for parts in json.loads(result):
            url = domian + parts[4]
            yield url

    # Получаем ссылки на все части света где есть магазины
    def get_parts_in_world():
        url = 'http://storelocator.yves-rocher.com/fr/'
        pattern = r"var store_list = (.*)]];"
        for url in get_data_in_page(url, pattern):
            print(url)
            yield url

    # Получаем ссылки на все страны где есть магазины
    def get_country_in_parts():
        pattern = r"var store_list = (.*)]];"
        for url_parts_in_world in get_parts_in_world():
            for url_country_in_parts in get_data_in_page(url_parts_in_world, pattern):
                print('---COUNTRY URL ---')
                print(url_country_in_parts)
                print('---END COUNTRY URL ---')
                yield url_country_in_parts

    # Получаем ссылки на все регионы где есть магазины
    def get_region_in_country():
        pattern = r"var store_list = (.*)]];"
        for url_country_in_parts in get_country_in_parts():
            if '/fr/europe/italy/' in url_country_in_parts:
                # Todo Италия Отдельный парсер
                print('ДЛЯ ИТАЛИИ ОТДЕЛЬНЫЙ ПАРСЕР')
                continue
            for url_region_in_country in get_data_in_page(url_country_in_parts, pattern):
                print('---REGION URL ---')
                print(url_region_in_country)
                print('---END REGION URL ---')
                yield url_region_in_country

    # Получаем ссылки на все города где есть магазины
    def get_city_in_region():
        pattern = r"var store_list = (.*)]];"
        for url_region_in_country in get_region_in_country():
            if '/fr/europe/france/centre/' in url_region_in_country:
                # Франция центр на сайте нет данных
                print('Франция центр на сайте нет данных')
                continue
            for url_city_in_region in get_data_in_page(url_region_in_country, pattern):
                print('---CITY URL ---')
                print(url_city_in_region)
                print('---END CITY URL ---')
                yield url_city_in_region



    def search_data_in_page(page,x,y):
        page = BeautifulSoup(page, 'html.parser')
        mycdblocationdetails = page.find('div', id='mycdblocationdetails')
        address = mycdblocationdetails.find('span', id='address').text
        phone = mycdblocationdetails.find('div', id='contacts').text
        phone = phone.replace('Téléphone :','')
        phone = phone.replace('Accéder au site du magasin','')
        phone = phone.strip()
        address = address.strip()

        store_dict = {
            'address': address,
            'phone': phone,
            'x': x,
            'y': y,
            'brand_name': 'Yves Rocher',
            'holding_name': 'Yves Rocher',
            'website': 'http://storelocator.yves-rocher.com/fr/',
            'date_review': datetime.datetime.now(),
        }
        print(store_dict)
        all_shops.append(store_dict)





    def search_shops(url_city_in_region):
        print(url_city_in_region)

        if 'http://storelocator.yves-rocher.com/fr/europe/italy/lombardia/milano/milano-stazione-centrale/' in url_city_in_region:
            print('ИТАЛИЯ')
        elif 'http://storelocator.yves-rocher.com/fr/europe/italy/lombardia/rozzano/rozzano/' in url_city_in_region:
            print('ИТАЛИЯ')
        else:
            r = requests.get(url_city_in_region)

            if r.status_code == 200:
                r = r.text
                pattern = r"var store_list = (.*)]];"
                result = re.findall(pattern, r)
                # ЕСЛИ НА СТРАНИЦЕ НЕ НАЙДЕН СПИСОК СО СЫЛКАМИ НА ДРУГИЕ МАГАЗИНЫ ТО ЭТО КОНЕЧНАЯ ТОЧКА
                if result == []:

                    print('ЭТО КОНЕЧНАЯ ТОЧКА')
                    y = re.findall(r"var lat = (.*);", r)[0]
                    x = re.findall(r"var lng = (.*);", r)[0]
                    search_data_in_page(r, x, y)

                else:
                    print(result)
                    result = result[0] + ']]'
                    for parts in json.loads(result):
                        url = domian + parts[4]
                        search_shops(url)
            else:
                print('BAD_PAGE')


    def get_shop_in_city():
        for url_city_in_region in get_city_in_region():
            search_shops(url_city_in_region)

    get_shop_in_city()

# Функция для записи в XLSX не вызываетя ( закомпилирована ) см. maria_pd_data
def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def yves_pd_data():
    """

    :return:
    """

    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'yves')
    return df



yves_pd_data()
