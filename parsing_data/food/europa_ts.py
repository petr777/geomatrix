import requests
from bs4 import BeautifulSoup
import re

def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page



def get_coord(page):
    page = page.prettify()
    result = re.findall(r'"coords":\[(.*?)],', page)[0]
    x, y = result.split(',')
    print(x, y)
    return x, y

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
    # TODO ПРОВЕРИТЬ
    x, y = get_coord(detail_page)

    time_work = get_time_work(detail_page)
    tel = get_tel(detail_page)
    print(name)
    print(address)
    print(time_work)
    print(tel)
    #print(detail_href)
