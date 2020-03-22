import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime


def get_page(url):
    print(url)
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page


def get_detail_data(html):
    phone = html.find('a', class_='phone phone-adress').text
    worktime = html.find('span', class_='worktime').text
    worktime = worktime.replace('\n', '')
    worktime = worktime.replace('\r', ' ')
    # Заменяем два пробела на один
    worktime = worktime.replace('  ', ' ')
    return phone, worktime

def get_data():
    all_shop = []

    def get_shop_in_city(id, name_city):
        url = f'https://www.maxidom.ru/shops/?city-id={id}'
        page = get_page(url)
        fragment = page.find('div', id='content-maxi')
        all_shop_in_city = fragment.find("nav", class_='nav-adress').find_all('ul')
        for ul in all_shop_in_city:
            for shop in ul.find_all('li'):
                address = shop.text.strip()
                # Находим магазин по id
                name_atr = shop['id'].lower()
                name_atr = 'div_' + name_atr
                detail_data = page.find('div', {name_atr: '1'})
                # отправляем рагмент html в фунцию для детального разбора
                phone, worktime = get_detail_data(detail_data)
                store_dict = {
                    'city':name_city,
                    'address': address,
                    'working_time': worktime,
                    'phone': phone,
                    'x': shop['attr-lon'],
                    'y': shop['attr-lat'],
                    'brand_name': 'Maxidom',
                    'holding_name': 'Maxidom',
                    'website': 'https://www.maxidom.ru/shops/',
                    'date_review': datetime.datetime.now(),
                }
                all_shop.append(store_dict)


    def get_all_city():
        page = get_page('https://www.maxidom.ru/shops/')
        all_city = page.find('div', class_='wrap-block-adress').find('div', class_='select-button-box')
        all_city = all_city.find('ul').find_all('li')
        for city in all_city:
            id_city = city.a['attr-id']
            name_city = city.a.text
            if 'Регионы РФ' in name_city:
                continue
            get_shop_in_city(id_city, name_city)

    get_all_city()
    return all_shop



def maxidom_pd_data():
    """
    1. Отправляем запрос по адресу https://www.maxidom.ru/shops/ далее средствами bs4 находим id и мена всех городов
    2. Циклом перебираем найденное если  имя города == Регионы РФ проускаем если нет то отпраляем id города и имя в
       функцию get_shop_in_city
    3. в Функции get_shop_in_city() отпраяляем запрос по url 'https://www.maxidom.ru/shops/?city-id={id}' подставляя
       соответствуюший id
    4. На полученной странице средствами bs4 находим фрагмент где соодержатся координаты и id магазина
    5. Для получения времении работы и телефона отпраляем фрагмент html функцию get_detail_data()
       - где средствами bs4 и манипуляций с текстом забираем  phone, worktime.
    6. Формируем store_dict который записываем в all_shop = []
    7. Возврашаем all_shop = [] в функцию maxidom_pd_data(), где формируем DF

    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df