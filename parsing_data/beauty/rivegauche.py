import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd
from pandas import ExcelWriter


def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_coords(url):
    page = get_page(url).text
    try:
        result = re.findall(r'"latlons":\[\[(.*?)]],', page)[0]
        coords = result.split(',')[:2]
        y, x = coords
        y = y.replace('"',"")
        x = x.replace('"',"")
        return y, x
    except:
        return None, None

def get_address(html):
    text_adres = ""
    address = html.find('div', class_="padding")
    for row in address.text.split('\n'):
        if '+7' in row:
            pass
        elif ':00' in row:
            pass
        else:
            text_adres += row.strip()
    return text_adres


def get_data():

    domian = 'http://www.rivegauche.ru'
    all_shop = []
    def search_data(shop):
        detail_page_url = shop.find('a', class_='shop-page-link')['href']
        detail_page_url = domian + detail_page_url
        print(detail_page_url)
        y, x = get_coords(detail_page_url)
        shops_container = shop.find('div', class_="shopsContainer")



        subway = shops_container.find('span', class_="subway")
        name_TC = shops_container.find('span', class_="filter-title")
        phone = shops_container.find('div', class_="field-item odd")

        address = get_address(shops_container)



        if subway is not None:
            subway = subway.text.strip()
            address = address.replace('м.', '')
            address = address.replace(subway, '')

        if name_TC is not None:
             name_TC = name_TC.text.strip()
             address = address.replace(name_TC, '')

        if phone is not None:
            phone = phone.text.strip()

        time_work = None
        for row in shops_container.text.split('\n'):
            if ':00' in row:
                time_work = row.strip()

        store_dict = {
            "address": address,
            'subway': subway,
            'name_TC': name_TC,
            "phone": phone,
            "time_work": time_work,
            "x": x,
            "y": y,
            'brand_name': "Rive Gauche",
            'holding_name': "Rive Gauche",
            'website': 'http://www.rivegauche.ru/shops',
            'date_review': datetime.datetime.now(),
        }
        print(store_dict)
        all_shop.append(store_dict)

    def get_shop_in_city(url):
        page = get_page(url)
        content = page.find('div', id="content")
        city_name = content.find('div', class_='paddings').find('h1').text
        print(city_name)
        if content.find('div', {"class": "view-content"}) == None:
            print(f'в регионе {city_name} по ссылку {url} нет магазинов')
        else:
            shops = content.find('div', {"class": "view-content"}).find_all('div', {"class": "node"})
            print(len(shops))
            for shop in shops:
                search_data(shop)

    def get_all_city():
        start_page = get_page('http://www.rivegauche.ru/shops')
        for li in start_page.find('table', class_="city").find_all('li')[1:]:
            url = domian + li.a['href']
            get_shop_in_city(url)

    get_all_city()
    return all_shop

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def letu_pd_data():
    """

    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'Rive Gauche')
    return df

letu_pd_data()