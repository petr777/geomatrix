import requests
import pandas as pd
from pandas import ExcelWriter
import datetime

def clean_working_time(openingHours):
    text_openingHours = ''
    for day in openingHours:
        if day.get('closed') == True:
            text_openingHours += f'{ day["weekDay"]}: closed;'
        else:
            text_openingHours += f'{ day["weekDay"]}: {day["openAt"]} - {day["closeAt"]};'
    return text_openingHours

def get_data():
    all_data = []
    def get_all_stores(url):
        data = requests.get(url).json()
        all_stores = data['_embedded']['items']
        for store in all_stores:
            store_dict = {
                    'region': store['region'],
                    'city': store['city']['title'],
                    'address': store["address"],
                    'working_time': clean_working_time(store['openingHours']),
                    'x': store['geoCoordinates'][0],
                    'y': store['geoCoordinates'][1],
                    'brand_name': 'Ulibka Radugi',
                    'holding_name': 'Ulibka Radugi',
                    'website': 'https://www.r-ulybka.ru/stores/',
                    'date_review': datetime.datetime.now(),
                }
            all_data.append(store_dict)

    # Делаем запросы по url выстатвии limit 100 одним запросом не отдает более 1000 поэтому перебираем странички
    limit = 100
    for num_page in range(1, 13):
        url = f'https://delivery.shop.api.svs.tdera.ru/stores?limit={limit}&page={num_page}'
        get_all_stores(url)
    return all_data

def r_ulybka_pd_data():
    """
    1. https://delivery.shop.api.svs.tdera.ru/stores?limit={limit}&page={num_page} отправляем запрос на страницу
    выставляя лимит и номер страницы
    2. Полученный ответ разбираем записываем магазины all_data = []
    3. Возврашаем all_data в функцию r_ulybka_pd_data
    4. Формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df


