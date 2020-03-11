import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import datetime
import json
import time



# TODO БАНЯТ ВОЗМОЖНО ДОСТАТОЧНО МЕНЯТЬ User-Agent или увеличтть sleep
def get_data():
    all_shop = []

    def get_coords(url):
        r = requests.get(url)
        page = BeautifulSoup(r.text, 'html.parser')
        try:
            coords = page.find('div', id='hypermarket-map')['data-addresses']
            coords = json.loads(coords)[0]
            x, y = coords[0], coords[1]
            return x, y
        except:
            return None


    def get_shop_href(ru_name_city, en_name_city):
        url = 'https://www.samberi.com'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Cookie": f"PHPSESSID=d6106f3e60ea45829e858773c7bba220; BITRIX_SM_GUEST_ID=1964409; _ym_uid=1583681473585127485; _ym_d=1583681473; _ym_wasSynced=%7B%22time%22%3A1583681472703%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; _ym_visorc_50321326=w; _fbp=fb.1.1583681472845.78912822; _ym_isad=2; _ym_visorc_46634277=w; BITRIX_SM_LAST_VISIT=09.03.2020+01%3A31%3A36;"
                      f" user_city={en_name_city}"
        }
        r = requests.get(url, headers=headers)
        page = BeautifulSoup(r.text, 'html.parser')
        # ВСЕ МАГАЗИНЫ В ГОРОДЕ
        print(ru_name_city)
        for shops in page.find('div', class_="nano-content").find_all('a'):
            time.sleep(10)
            coords = get_coords('https://www.samberi.com' + shops['href'])
            if coords is None:
                y, x = None, None
            else:
                y, x = coords[0], coords[1]

            store_dict = {
                'city': ru_name_city,
                'address': shops['data-address'],
                'bus_station': shops["data-bus_station"],
                'working_time': shops["data-schedule"],
                'x': x,
                'y': y,
                'brand_name': 'Samberi',
                'holding_name': 'Samberi',
                'website': 'https://www.samberi.com',
                'date_review': datetime.datetime.now(),

            }
            print(store_dict)
            all_shop.append(store_dict)


    def get_all_city():
        url = 'https://www.samberi.com'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }
        r = requests.get(url, headers=headers)
        page = BeautifulSoup(r.text, 'html.parser')
        for city in page.find('div', class_='change-city-btns').find_all('button'):
            time.sleep(5)
            ru_name_city = city.text.strip()
            en_name_city = city['data-city']
            get_shop_href(ru_name_city, en_name_city)

    get_all_city()
    return all_shop

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'


def samberi_pd_data():
    """
    1. в функции get_all_city() отправляем запрос на страницу https://www.samberi.com на которой средствамми bs4
       ---  page.find('div', class_='change-city-btns').find_all('button'): ---
       ищем все города ( Название Кирилицие и эквивалентное латиницей)
    2. Передаем название городов в функцию get_shop_href(), где название города латиницей подставляем в Cookie
    3. Отправляем запрос на страницу 'url = 'https://www.samberi.com' с замененеым текушим городом
    4. Разбираем полученную страницу средсвами bs4 ишем ссылку на конкреттный магазин
     ----- page.find('div', class_="nano-content").find_all('a') ----

    5. В сслыке под разными параметрами присутсвует вся интересуюшая информация за исключение координат, для получения
    которых отпарвляем url  в функцию
    6. Где средствами bs4 ищем текушие координаты page.find('div', id='hypermarket-map')['data-addresses']
    7. Записываем все данные all_shop = []
    8.Возвращаем all_shop в функцию samberi_pd_data в переменную good_data
    9. из good_data формируем DF

    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'Samberi')
    return df

samberi_pd_data()
