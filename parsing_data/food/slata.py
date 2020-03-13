import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_all_href_city():
    start_page = get_page('https://www.slata.ru/addresses/')
    all_city_list = []
    for li in start_page.find('ul', class_='address-city-list').find_all('li'):
        dict_city = {
            'name': li.text.strip(),
            'url': 'https://www.slata.ru/addresses/' + li.find('a')['href']
        }
        all_city_list.append(dict_city)
    return all_city_list

def get_data():
    good_data = []
    all_city = get_all_href_city()
    for city in all_city:
        print(city['name'])
        page = get_page(city['url'])
        for li in page.find('ul', class_='map-list-adress').find_all('li', class_="map-item-adress"):
            y, x = li['data-coord'].split(',')
            address = li.find('div', class_='map-address_text-1').text.strip()
            if li.find('div', class_='map-address_text-2') != None:
                name_TC = li.find('div', class_='map-address_text-2').text.strip()
            else:
                name_TC = None
            workin_time = li.find('div', class_='map-address_text-4 item').text.strip()
            tel = li.find('a').text
            store_dict = {
                'address': address,
                'shopping center': name_TC,
                'phone': tel,
                'working_time': workin_time,
                'x': x,
                'y': y,
                'brand_name': 'Slata',
                'holding_name': 'Slata',
                'website': 'https://www.slata.ru/addresses',
                'date_review': datetime.datetime.now(),
            }
            print(store_dict)
            good_data.append(store_dict)

    return good_data


def slata_pd_data():
    """
    1. в функции get_all_href_city() средствами bs4 полчаем имена и ссылки по каждому городу
    2. в функции get_data() перебираем ссылки с полученными городами
    3. средставми bs4 ищем всю интересующую информацию
    4. записываем каждый магазин в  список good_data
    5. из good_data формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df
