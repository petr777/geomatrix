import requests
import pandas as pd
from pandas import ExcelWriter
from bs4 import BeautifulSoup
import datetime
import json

main_domian = 'http://доброцен.рф'

def search_data_markers(page):
    ul = page.find('div', id='ul-content')
    #print(ul)
    list_region = ul.find('div', {"data-contents": "true"})
    all_address_shops_in_region = list_region.find_all('ul')


    print(len(all_address_shops_in_region))
    print(len(list_region.find_all('div', {'class': '_17fgIIn___block normal'})))


    """
    data_markers = ul.find('div', class_='ul-widget ul-widget-maps')
    list_shops = json.loads(data_markers['data-markers'])
    for shop in list_shops:
        print(shop)
    """
    return True


def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

start_page = get_page('http://доброцен.рф/adriesa_maghazinov')
href_coyntrys = start_page.find_all('span', 'LreJDHx___wrapper')

for href_coyntry in href_coyntrys:
    name_coyntry = href_coyntry.a.text
    url_coyntry = main_domian + href_coyntry.a['href']
    print(name_coyntry)
    print(url_coyntry)
    coyntry_page = get_page(url_coyntry)
    search_data_markers(coyntry_page)





# TODO найти нас тарицу России, Беларуссии перейти на страницу фед. округа
# далее на старницы фед окрыга ишии с помошь bs4 <div id="ul-content">


