import requests
import re
import json
import ast
import pandas as pd
from pandas import ExcelWriter
import datetime

def get_id_session(s):
    r = s.get('https://www.letu.ru/stores?')
    result = re.findall(r"sessionStorage.setItem\('_dynSessConf',(.*)\);", r.text)[0]
    result = result.replace("'","").strip()
    return result

"""

# ФУНКЦИЯ ПОЛУЧАЕ ID ГОРОДОВ ПОСТОЯННЫЙ ЗАПУСК НЕ ТРЕБУЕСЯ
def get_all_city_id():
    s = requests.Session()
    id_session = get_id_session(s)
    all_city = []
    uniq_city = set()

    # --- КОНСТАНТА --- #
    moscow = {'id': 8113, 'name': 'Москва (в пределах МКАД)'}
    uniq_city.add(moscow['name'])
    all_city.append(moscow)
    # ------------------#

    for id_city in range(0, 100000):
        url = f"https://www.letu.ru/rest/model/atg/rest/geolocation/actor/GeolocationActor/setGeolocationInfo?pushSite=storeMobileRU&locale=ru_RU&cityId={id_city}&pushSite=storeMobileRU&_dynSessConf={id_session}"
        resp = s.get(url)
        JSON = json.loads(resp.text)
        result = JSON['result']
        if result['name'] not in uniq_city:
            uniq_city.add(result['name'])
            city = {
                'id': id_city,
                'name': result['name']
            }
            all_city.append(city)
            print(city)
        else:
            print(f'{result["name"]} - уже есть')

    f = open('all_city_letu.txt', 'w')
    for item in all_city:
        f.write(f"{item}\n")
    f.close()
"""

def get_data():
    all_shop = []

    def cleanre_data(store, city_name):
        print(store)
        store_dict = {
            'name': store['storeName'],
            'storeType': store['storeType'],
            'city': city_name,
            'subway': store.get('subway'),
            'address': store["addressShort"],
            'working_time': store['openHours'],
            'phone': store['phoneNumber'],
            'x': store['longitude'],
            'y': store['latitude'],
            'brand_name': "L'Etoile",
            'holding_name': "L'Etoile",
            'website': 'https://www.letu.ru/',
            'date_review': datetime.datetime.now(),
        }
        all_shop.append(store_dict)

    def get_data_in_city():
        f = open('all_city_letu.txt', 'r')
        s = requests.Session()
        id_session = get_id_session(s)
        for row in f.readlines():
            dict_city = ast.literal_eval(row)
            print(dict_city)
            id_city = dict_city['id']
            city_name = dict_city['name']
            resp = s.get(f'https://www.letu.ru/rest/model/atg/rest/geolocation/actor/GeolocationActor/geolocationStoresByCity?pushSite=storeMobileRU&locale=ru_RU&storeType=store&cityId={id_city}&isUIVisible=&isScentBibliotheque=false&hasMakeupExpert=false&pushSite=storeMobileRU&_dynSessConf={id_session}')
            JSON = json.loads(resp.text)
            for shop in JSON['result']['geolocationStoreInfoList']:
                cleanre_data(shop, city_name)

    #get_all_city_id()
    get_data_in_city()
    return all_shop

def letu_pd_data():
    """
    - для коректных запросов нам понадобится номер сессии который получаем с помошью функции get_id_session()
    - ЕСЛИ раскоментировать строку 85  #get_all_city_id()  запустится пункт 1 он не обязателен


    1. Функция  get_all_city_id() служит для получения списка всех городов не обязательночто там есть магазины но
       внутрений посковик сайта выдает их, остаточно один раз получить список всех городов и id к ним
       - получаем номер сесси
       - циклом отправляем запросы по адресу подставляя номер сессии id_city:
        "https://www.letu.ru/rest/model/atg/rest/geolocation/actor/GeolocationActor/setGeolocationInfo?pushSite=storeMobileRU&locale=ru_RU&cityId={id_city}&pushSite=storeMobileRU&_dynSessConf={id_session}"
       - записываме все уникальные города с их id  в файл all_city_letu.txt

    2. В функции get_data_in_city() читаем острочно файл all_city_letu.txt
       - получаем номер сесси
       - отправляем запрос в ответ приходят магазины в указанном городе
       - resp = s.get(f'https://www.letu.ru/rest/model/atg/rest/geolocation/actor/GeolocationActor/geolocationStoresByCity?pushSite=storeMobileRU&locale=ru_RU&storeType=store&cityId={id_city}&isUIVisible=&isScentBibliotheque=false&hasMakeupExpert=false&pushSite=storeMobileRU&_dynSessConf={id_session}')
       - разбираем JSON и отправлем каждый магазин в функцию  cleanre_data()
       - Формируем коректный dict оторый записываем в  all_shop = []
       - возврашаем  all_shop  в функцию letu_pd_data

    3. Формируем df
    :return:
    """

    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df

