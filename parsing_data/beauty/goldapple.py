from selenium import webdriver
import time
from bs4 import BeautifulSoup
import datetime
from pandas import ExcelWriter
import pandas as pd

def get_page():
    driver = webdriver.Chrome()
    driver.get('https://goldapple.ru/stockists')
    time.sleep(5)
    page = driver.page_source
    driver.close()
    return page


def get_data():
    all_shop = []
    page_html = get_page()
    page = BeautifulSoup(page_html, 'html.parser')
    stores_content = page.find('div', class_='stores__content').find_all('div', {'class':'row'})
    for store in stores_content:
        fragment = store.find('div', {'class':'stores-additional-content'})
        coords = store.find('div', class_={'stores__map map'})

        city = store['data-city']
        y = coords['data-lat']
        x = coords['data-lng']

        address = fragment.find('p', {'class':'store-address'} )
        name_TC = fragment.find('p', {'class':'store-molls-name'} )
        working_time = fragment.find('p', {'class':'store-schelude'} )
        phone = fragment.find('p', {'class':'store-phone'})
        if address is not None:
            address = address.text
        if name_TC is not None:
            name_TC = name_TC.text
        if working_time is not None:
            working_time = working_time.text
        if phone is not None:
            phone = phone.text

        store_dict = {
            'city': city,
            'address': address,
            'name_TC': name_TC,
            'working_time': working_time,
            'phone': phone,
            'x': x,
            'y': y,
            'brand_name': 'Zolotoy Yabloko',
            'holding_name': 'Zolotoy Yabloko',
            'website': 'https://goldapple.ru/stockists',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)

    return all_shop


def goldapple_pd_data():
    """
    1. Открываем https://goldapple.ru/stockists средствами seleniun читаем открывшуюся страницу и разбирем html
    2. Средствами bs4 находим все интересуюшие данные записываем их в переменную all_shops
    3. Возврашаем all_shops в goldapple_pd_data
    4. Формируем df из всех получееных данных
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df

