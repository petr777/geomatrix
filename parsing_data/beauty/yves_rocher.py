import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd


def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def pars_table_working_time(table):
    working_time_end = ''
    for day_row in table.find_all('tr'):
        day = day_row.find_all('td')[0].text
        working_time = day_row.find_all('td')[1].text
        working_time_end += f'{day}-{working_time};'
    return working_time_end

def get_data():
    all_shop = []
    def get_detail_shop(name_region, url):
        page = get_page(url)
        data = page.find('dl', class_='first nng_address')
        table_working_time = page.find('table', class_="horaire-table")
        working_time = pars_table_working_time(table_working_time)
        # Адаляем не нужный tag
        data.dt.decompose()

        # Находим ссылку на гугл карту забираем координаты
        map_row = data.find_all('dd')[1]
        url_map = map_row.find('a')['href']
        coords = url_map.split('=')[-1]
        y, x = coords.split(',')

        # Преобразовываем фрагмент html в строку удаляем все теги, а br заменяем на перенос сторки
        address_row = data.find_all('dd')[0]
        address_row = str(address_row)
        address_row = address_row.replace('<br/>', '\n')
        address_row = address_row.replace('</dd>', '').replace('<dd>', '')
        address_list = address_row.split('\n')

        address = None
        name_TC = None
        post_code_row = None

        # Если есть название ТЦ то три элемента в списке если нет то 2
        if len(address_list) == 3:
            address = address_list[0]
            name_TC  = address_list[1]
            post_code_row = address_list[2]
        elif len(address_list) == 2:
            address = address_list[0]
            post_code_row = address_list[1]

        # С помошью регулрок забираем имя города и почтовый индекс
        post_code_list = re.findall(r'(\w+)', post_code_row)
        post_code, name_city = post_code_list[0], post_code_list[1]

        store_dict = {
            'region': name_region,
            'city': name_city,
            'post_code': post_code,
            'address': address,
            'name_TC': name_TC,
            'working_time': working_time,
            'x': x,
            'y': y,
            'brand_name': 'Yves Rocher',
            'holding_name': 'Yves Rocher',
            'website': 'http://storelocator.yves-rocher.com/fr/',
            'date_review': datetime.datetime.now(),
        }
        print(store_dict)

        all_shop.append(store_dict)

    start_url = 'https://www.yves-rocher.ru/butik/butiki-i-instituty-krasoty/SL'
    page = get_page(start_url)
    all_shops = page.find('div', id='main_togglable').find('ul')
    for child in all_shops.children:
        name_region = child.h3.text
        name_region = name_region.replace('Бутики и SPA-Салоны:', '').strip()
        print(name_region)
        for shop in child.ul.find_all('li'):
            url = 'https://www.yves-rocher.ru'+ shop.find('a')['href']
            get_detail_shop(name_region, url)

    return all_shop



def yves_pd_data():
    """
    1. Переходим по url 'https://www.yves-rocher.ru/butik/butiki-i-instituty-krasoty/SL'
    2. Средствами bs4 получаем наименование и ссылки на все магазины
    3. Отправляем url в функцию  get_detail_shop(), где посещаем страницу конкретоного магазина
       - средствами bs4 и регулярных выражений находим данныем СМ. get_detail_shop()
         ### постарался описать пошагово ###
    4. записываем данные по магазину в all_shop = [] , который возврашаем в функцию yves_pd_data()
    5. форируем DF из данных

    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df