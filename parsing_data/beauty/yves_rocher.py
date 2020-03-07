from bs4 import BeautifulSoup
import requests
import re
import json

def get_parts_in_world():
    # Получаем ссылки на все части света где есть магазины
    r = requests.get('http://storelocator.yves-rocher.com/fr/')
    result = re.findall(r"var store_list = (.*)]];", r.text)[0] + ']]'
    list_url_parts = []
    for parts in json.loads(result):
        list_url_parts.append(parts[4])
    print('Получили все части света')
    return list_url_parts

def get_country_in_parts():
    # Получаем ссылки на все страны  где есть магазины
    list_url_parst = get_parts_in_world()
    list_url_country = []
    for parts in list_url_parst:
        r = requests.get(f'http://storelocator.yves-rocher.com{parts}')
        result = re.findall(r"var store_list = (.*)]];", r.text)[0] + ']]'
        for country in json.loads(result):
            list_url_country.append(country[4])
        print(f'Получили все страны по ссылке {country[4]}')
    return list_url_country

def get_region_in_country():
    # Получаем ссылки на все регионы где есть магазины
    list_url_country = get_country_in_parts()
    list_url_region = []
    for country in list_url_country:
        if '/fr/europe/italy/' == country:
            # Todo Италия Отдельный парсер
            pass
        else:
            r = requests.get(f'http://storelocator.yves-rocher.com{country}')
            result = re.findall(r"var store_list = (.*)]];", r.text)[0] + ']]'
            for region in json.loads(result):
                list_url_region.append(region[4])
                print(f'Получили все регионы по ссылке {region[4]}')
    return list_url_region

def get_city_in_region():
    # Получаем ссылки на все города где есть магазины
    list_url_region = get_region_in_country()
    list_url_city = []
    for region in list_url_region:
        print(f'Регион-{region}')
        if region == '/fr/europe/france/centre/':
            # Франция центр на сайте нет данных
            pass
        else:
            r = requests.get(f'http://storelocator.yves-rocher.com/{region}')
            result = re.findall(r"var store_list = (.*)]];", r.text)[0] + ']]'
            for city in json.loads(result):
                print(city)
                list_url_city.append(city[4])
                print(f'Получили все города по ссылке {city[4]}')
    return list_url_city


def get_stores_in_city():
    list_url_city = get_city_in_region()
    list_url_stores = []
    # Todo если это прямая ссылка на магазин парсим если нет то:
    for city in list_url_city:
        print(f'Город-{city}')
        r = requests.get(f'http://storelocator.yves-rocher.com/{city}')
        result = re.findall(r"var store_list = (.*)]];", r.text)[0] + ']]'
        for store in json.loads(result):
            print(store)
            list_url_stores.append(store[4])
            print(f'Получили все города по ссылке {store[4]}')


print(get_stores_in_city())