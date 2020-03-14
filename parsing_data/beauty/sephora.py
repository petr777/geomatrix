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
    def get_stores_in_city(url):
        page = get_page(url)
        slick_list = page.find('div', class_="b-shops__slider _js_shops-slider")
        slick_list = slick_list.find_all('div', class_="b-shops__slider-item")
        for shop in slick_list:
            city = shop.find('div', class_="b-shops__slider-item-city").text.strip()
            name = shop.find('div', class_="b-shops__slider-item-name").text.strip()
            coords = ast.literal_eval(shop['data-coords'])
            data = shop.find('div', class_="b-shops__slider-item-contacts").text.strip()

            time_work = None
            address = None
            phone = None

            for row in data.split('\n'):
                if ':00' in row:
                    time_work = row.strip()
                    time_work = time_work.replace('Открыто: ', '')
                elif 'Адрес: ' in row:
                    address = row.strip()
                    address = address.replace('Адрес: ', '')
                elif 'Тел.: '  in row:
                    phone = row.strip()
                    phone = phone.replace('Тел.:', '')
                else:
                    pass

            store_dict = {
                'city': city,
                'name': name,
                'address': address,
                'working_time': time_work,
                'phone': phone,
                'x': coords[1],
                'y': coords[0],
                'brand_name': 'Sephora',
                'holding_name': 'LVMH',
                'website': 'http://www.ugdvor.ru/',
                'date_review': datetime.datetime.now(),
            }
            print(store_dict)
            all_shop.append(store_dict)

    def get_all_city():
        start_page = get_page('https://sephora.ru/company/shops/')
        for city in start_page.find('div', class_="b-shops-cities__items").find_all('a'):
            url = 'https://sephora.ru/company/shops/' + city['href']
            get_stores_in_city(url)

    get_all_city()
    return all_shop


def write_xlsx(df, name_file):
    writer = ExcelWriter(f'xlsx\{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def sephora_pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'sephora')
    return df

sephora_pd_data()
