import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
from pandas import ExcelWriter


def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page


def get_data():
    all_shop = []
    uniq_address = set()

    def get_data_in_city(city, url):
        page = get_page(url)
        fragmen = page.find('div', id='cityHelpAddressKontaktsInfo')
        address_list = fragmen.find('div', {'class': 'cityHelpAddress'}).find_all('div', class_='cityHelpAddressInnerAddress')
        fragmen_time_work = fragmen.find('div', class_='cityHelpAddressKontaktsAddress cityHelpWorkTime').find_all('div', class_='cityHelpAddressInnerText')

        for address_row in address_list:
            address = address_row.text

            if len(fragmen_time_work) == 5:
                working_time = fragmen_time_work[2].text
            else:
                working_time = fragmen_time_work[-2].text

            if address not in uniq_address:
                store_dict = {
                    'city': city,
                    'address': address,
                    'working_time': working_time,
                    'brand_name': 'Akson',
                    'holding_name': 'Akson',
                    'website': 'https://akson.ru/',
                    'date_review': datetime.datetime.now(),
                }
                all_shop.append(store_dict)
                uniq_address.add(address)




    def get_city():
        url = 'https://akson.ru/ajax/ajax_city_choise_new.php'
        page = get_page(url)
        uniq_city = set()
        for city in page.find('div', class_='new_city_choise_wrapper _akson-city-container').find_all('a'):
            name = city['data-name']
            name = name.replace(' Громова', '')
            name = name.replace(' Фрунзе', '')
            name = name.replace(' Болдина', '')
            href = city['href']
            href = href.replace('&TP_CITY_STORE=4', '')
            href = href.replace('&TP_CITY_STORE=15', '')
            href = href.replace('?TP_CITY_CODE=', '')
            if href not in uniq_city:
                url = f'https://akson.ru/help/adresa-i-kontakty/{href}'
                get_data_in_city(name, url)
                uniq_city.add(href)

    get_city()
    return all_shop

def get_coords():
    url = 'https://akson.ru/help/adresa-i-kontakty/moskva54/'
    r = requests.get(url)
    r1 = re.findall(r'new ymaps.Placemark\(\[(.*)]', r.text)
    r2 = re.findall(r"hintContent: '(.*)',", r.text)
    num_index = 0
    all_shop = []
    while num_index < len(r1):
        name = r2[num_index]
        y, x = r1[num_index].split(',')
        num_index += 1
        store_dict = {
            "name_ТС":name,
            'x': x,
            'y': y,
        }
        all_shop.append(store_dict)
    return all_shop

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'xlsx\{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'


def akson_pd_data():
    """
     Координаты отдельным DF;
     адреса, время работы, город отдельным DF
     m.к. наборы данных между собой никак несвязанны.

    ------- Поэтому получаем данные с адресами, временем работы, именами городов

    1. в функции  get_city() отправляем запрос https://akson.ru/ajax/ajax_city_choise_new.php
        - Разбираем ответ на ссылки к городам и их наименование
        - проверяем на уникальность, убираем ненужное, испраляем ошибки
    2. Циклом перебиреам олученный результат отправляем url  функцию  get_data_in_city()
       -  в текушей функции средствами bs4  находим адреса и время работы
    3. Формируем store_dict который записываем в all_shop = []
    4. Возврашаем all_shop = [] в функцию akson_pd_data(), где формируем DF

    --- и отдельно получаем набор координат и наименование ТЦ

    1. в функции get_coords() отправляем запрос по url = https://akson.ru/help/adresa-i-kontakty/moskva54/
    2. C помошью регулярных выражений находим наименоване всех ТЦ и их координаты
    3. Формируем store_dict который записываем в all_shop = []
    4. Возврашаем all_shop = [] в функцию akson_pd_data(), где формируем DF


    """
    coods_data = get_coords()
    good_data = get_data()
    df_data = pd.DataFrame(good_data)
    #write_xlsx(df_data, 'akson_pd_data')
    df_coords = pd.DataFrame(coods_data)
    #write_xlsx(df_coords, 'akson_pd_data_coords')
    return df_data, df_coords
