import requests
from bs4 import BeautifulSoup
import json
import time

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
        time.sleep(5)
        # TODO ПРОВЕРИТЬ
        coords = get_coords('https://www.samberi.com' + shops['href'])
        if coords is None:
            x = None
            y = None
        else:
            x = coords[0]
            y = coords[1]

        dict_shop = {
            'city': ru_name_city,
            'address': shops['data-address'],
            'bus_station': shops["data-bus_station"],
            'working_time': shops["data-schedule"],
            'x': x,
            'y': y,
        }
        print(dict_shop)


def get_all_city():

    url = 'https://www.samberi.com'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    }
    r = requests.get(url, headers =headers)
    page = BeautifulSoup(r.text, 'html.parser')
    for city in page.find('div', class_='change-city-btns').find_all('button')[4:]:
        time.sleep(3)
        ru_name_city = city.text.strip()
        en_name_city = city['data-city']
        get_shop_href(ru_name_city, en_name_city)




get_all_city()
