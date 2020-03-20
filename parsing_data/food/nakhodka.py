import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
import json


def get_yandex_map_url():
    r = requests.get('https://nahodka-magazin.ru/magaziny/')
    page = BeautifulSoup(r.text, 'html.parser')
    map = page.find('div', class_='this_map').iframe['src']
    return map


def get_point():
    url_yandex_map_url = get_yandex_map_url()
    r = requests.get(url_yandex_map_url).text
    stores_data_row = re.findall(r'provide\({"ymj":"1.0","maps":(.*),"presetStorage"', r)[0]
    JSON = json.loads(stores_data_row)
    points = [point['geoObjects']['features'] for point in JSON]
    for point in points[0]:
        print(point)

get_point()

