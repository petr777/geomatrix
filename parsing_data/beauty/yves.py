import requests
import re
import json

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
            print(url_country_in_parts)
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
            print(url_region_in_country)
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
            print(url_city_in_region)
            yield url_city_in_region



def get_shop_in_city():
    pattern = r"var store_list = (.*)]];"
    for url_city_in_region in get_city_in_region():
        print(url_city_in_region)
        for url_shop_in_city in get_data_in_page(url_city_in_region, pattern):
            print(url_shop_in_city)
            yield url_shop_in_city




