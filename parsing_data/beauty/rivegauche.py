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

def get_coords(url):
    page = get_page(url).text
    try:
        result = re.findall(r'"latlons":\[\[(.*?)]],', page)[0]
        coords = result.split(',')[:2]
        y, x = coords
        y = y.replace('"',"")
        x = x.replace('"',"")
        return y,x
    except:
        return None, None



def get_address(html):
    address = html.find('div', class_="padding")
    for row in address.text.split('\n'):
        print(row)

    #print(address)

def get_data():
    domian = 'http://www.rivegauche.ru'
    def search_data(shop):
        detail_page_url = shop.find('a', class_='shop-page-link')['href']
        detail_page_url = domian + detail_page_url
        print(detail_page_url)
        coords = get_coords(detail_page_url)
        shops_container = shop.find('div', class_="shopsContainer")
        address = get_address(shops_container)

        if shops_container.find('span', class_="subway") != None:
            subway = shops_container.find('span', class_="subway").text.strip()
        else:
            subway = None

        if shops_container.find('span', class_="filter-title") != None:
            name_TC = shops_container.find('span', class_="filter-title").text.strip()
        else:
            name_TC = None

        if shops_container.find('div', class_="field-item odd") != None:
            phone = shops_container.find('div', class_="field-item odd").text.strip()
        else:
            phone = None

        time_work = None
        for row in shops_container.text.split('\n'):
            if ':00' in row:
                time_work = row.strip()
        #print(time_work)



    def get_shop_in_city(url):
        page = get_page(url)
        content = page.find('div', id="content")
        city_name = content.find('div', class_='paddings').find('h1').text
        print(city_name)
        if content.find('div', {"class": "view-content"}) == None:
            print(f'в регионе {city_name} по ссылку {url} нет магазинов')
        else:
            shops = content.find('div', {"class": "view-content"}).find_all('div', {"class": "node"})
            for shop in shops:
                search_data(shop)

    def get_all_city():
        start_page = get_page('http://www.rivegauche.ru/shops')
        for li in start_page.find('table', class_="city").find_all('li')[1:]:
            url = domian + li.a['href']
            get_shop_in_city(url)


    get_all_city()

get_data()