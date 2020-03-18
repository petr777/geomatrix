import requests
import datetime
import pandas as pd



def get_openingHours(openingHours):
    if openingHours is not None:
        working_time = ''
        for day in openingHours['weekDayOpeningList']:
            weekDay = day["weekDay"]
            openingTime = day["openingTime"]["formattedHour"]
            closingTime = day["closingTime"]["formattedHour"]
            working_time += f'{weekDay}:{openingTime}-{closingTime};'
        return working_time
    else:
        return None

def get_data():
    all_shop = []
    def get_city(city):
        with requests.Session() as s:
            url = f'https://shop.rivegauche.ru/customer-location/set-session-city?code=&name={city["name"]}'
            s.get(url).json()
            data = s.get('https://shop.rivegauche.ru/store-finder/getPointOfServices').json()
            for store in data:
                store_dict = {
                        'name': store['name'],
                        'city': city["name"],
                        'region': city["region"]['name'],
                        'address': store["line1"],
                        'working_time': get_openingHours(store['openingHours']),
                        "phone": store['phone1'],
                        'x': store['point']['longitude'],
                        'y': store['point']['latitude'],
                        'brand_name': 'Rive Gauche',
                        'holding_name': 'Rive Gauche',
                        'website': 'https://shop.rivegauche.ru/',
                        'date_review': datetime.datetime.now(),
                    }
                print(store_dict)
                all_shop.append(store_dict)


    def get_city_name():
        r = requests.get('https://shop.rivegauche.ru/rest/v1/newRG/city/citylist?countryCode=RU').json()
        for latter in r['sorted']:
            for city in latter[1]['cities']:
                print(city)
                get_city(city)

    get_city_name()
    return all_shop


def rivegauche_pd_data():
    """
    1. по url https://shop.rivegauche.ru/rest/v1/newRG/city/citylist?countryCode=RU  отправляем запрос на страницу
    получаем все города в алфавитном порядке
    2. Забираем имя города и отправляем в функцию get_city():
       - В текушей функции инициируе сесею сначала переходим по адресу
         url = f'https://shop.rivegauche.ru/customer-location/set-session-city?code=&name={name_city}'
         подставиви name_city тодействие азначает город в котором мы находимся
       - Далее отправляем запрос https://shop.rivegauche.ru/store-finder/getPointOfServices  ответ приходят магазины
         в текушем городе
       - Формируем коректный store_dict = {} записываем магазины в all_shop = []
    3. Возврашаем all_data в функцию rivegauche_pd_data
    4. Формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df


