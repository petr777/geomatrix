import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import datetime
import re

def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_coord(page):
    page = page.prettify()
    result = re.findall(r'"coords":\[(.*?)],', page)[0]
    y, x = result.split(',')
    return y, x


def get_time_work(page):
    try:
        time_work = page.find('div', class_='field field-name-field-timework field-type-text field-label-hidden').text
        return time_work.strip()
    except:
        return None

def get_tel(page):
    try:
        time_work = page.find('div', class_='field field-name-field-tel field-type-text field-label-hidden').text
        return time_work.strip()
    except:
        return None


def get_data():
    all_shop = []
    start_page = get_page('https://europa-ts.ru/ru/tcenters')
    all_shops = start_page.find('div', class_='view-content').find_all('div', class_='views-row')
    for shop in all_shops:
        address = shop.find('div', class_="views-field views-field-field-adress").text.strip()
        name = shop.find('div', class_="views-field views-field-title").text.strip()
        detail_href = shop.find('div', class_="views-field views-field-title").a['href']
        detail_href = 'https://europa-ts.ru' + detail_href

        # Переходим на страницу конкретного магазина
        detail_page = get_page(detail_href)
        print(detail_href)
        y, x = get_coord(detail_page)
        store_dict = {
            'name': name,
            'address': address,
            'working_time': get_time_work(detail_page),
            'x': x,
            'y': y,
            'phone': get_tel(detail_page),

            'brand_name': 'Evropa',
            'holding_name': 'Evropa',
            'website': 'https://europa-ts.ru/ru/tcenters',
            'date_review': datetime.datetime.now(),
        }
        print(store_dict)
        all_shop.append(store_dict)
    return all_shop

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def europa_ts_pd_data():
    """
    1. Отправляем запрос по адрессу https://europa-ts.ru/ru/tcenters'
    2. Средствами bs4 start_page.find('div', class_='view-content').find_all('div', class_='views-row')
    находим инфу по всем магазинам
    3. Перебираем циклом забираем чать информации непосредствеен с главной страницы
        address, name, detail_href
    4. Для получениия координат необходим перейти непосредственно на страницу магазина что и делаем переходя по ссылке
        detail_href
        - На странице находим координаты, время работы, телефон
    5. Записываем все данные all_shop = []
    6. Возвращаем all_shop в функцию europa_ts_pd_data в переменную good_data
    7. из good_data формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    # write_xlsx(df, 'Evropa')
    return df




