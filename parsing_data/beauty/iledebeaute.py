import requests
from bs4 import BeautifulSoup
import re
import ast
import datetime
import pandas as pd
from pandas import ExcelWriter

domian = 'https://iledebeaute.ru'

def get_page(url):
    print(url)
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page



def get_data_one_shop(url):
    page_shop = get_page(url)
    if page_shop.find('div', {"class":"contacts"}) != None:
        address = page_shop.find('div', {"class":"contacts"}).find('span', {'itemprop':"streetAddress"})
        if page_shop.find('div', {"class":"contacts"}).find('span', {'itemprop':"streetAddress"}) != None:
            return address.text
        else:
            address = page_shop.find('div', {"class": "contacts"}).h3.text
            return address
    else:
        return None

def pars_name(name_shop):

    if 'SEPHORA' in name_shop:
        brand_name = 'SEPHORA'
        name_shop = name_shop.replace('SEPHORA,', '')
        name_shop = name_shop.replace('SEPHORA', '')
    elif 'ИЛЬ ДЕ БОТЭ' in name_shop:
        brand_name = 'ИЛЬ ДЕ БОТЭ'
        name_shop = name_shop.replace('ИЛЬ ДЕ БОТЭ,', '')
        name_shop = name_shop.replace('ИЛЬ ДЕ БОТЭ', '')
    else:
        brand_name = 'ИЛЬ ДЕ БОТЭ'

    subway = None
    shop_title = None

    name_shop_list = name_shop.split(',')
    for item in name_shop_list:
        if 'м. ' in item:
            subway = item
        else:
            shop_title = item

    return brand_name, shop_title, subway

def get_data():
    all_shop = []
    def all_shop_in_city(url, name_city):
        shops_in_city_page = get_page(url)
        table_data = shops_in_city_page.find('table', {"class": 'shops_list'})
        for shop in table_data.find_all('tr'):
            href = shop.find_all('td')[0].a['href']
            url = domian + href
            name_shop = shop.find_all('td')[0].a.text
            brand_name, shop_title, subway = pars_name(name_shop)
            working_time = shop.find_all('td')[1].text
            phone = shop.find_all('td')[2].text
            address = get_data_one_shop(url)
            store_dict = {
                'name': shop_title,
                'city': name_city,
                'subway': subway,
                'address': address,
                'working_time': working_time,
                'phone': phone,
                'x': None,
                'y': None,
                'brand_name': brand_name,
                'holding_name': "LVMH",
                'website': 'https://iledebeaute.ru',
                'date_review': datetime.datetime.now(),
            }
            print(store_dict)
            all_shop.append(store_dict)


    def get_all_city_url():
        start_page = get_page('https://iledebeaute.ru/company/shops/')
        for ul in start_page.find('div', {'class': 'all_shops'}).find_all('ul'):
            for li in ul.find_all('li'):
                if 'Online-магазин' not in li.a.text:
                    url = domian + li.a['href']
                    name_city = li.a.text
                    all_shop_in_city(url, name_city)

    get_all_city_url()
    return all_shop


def write_xlsx(df, name_file):
    writer = ExcelWriter(f'xlsx\{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def iledebeaute_pd_data():
    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'iledebeaute')
    return df

iledebeaute_pd_data()