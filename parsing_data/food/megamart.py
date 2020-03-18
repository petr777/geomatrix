from selenium import webdriver
import time
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_data():
    driver = webdriver.Chrome()
    all_shop = []

    def get_good_data(td_address_list, td_href_map_list, td_time_list):
        count = 0
        sizeOfList = len(td_address_list)
        while True:
            if count == sizeOfList:
                break
            else:
                print(f"{sizeOfList}-sizeOfList")
                print(f'{count}-count')
                shop = {
                    'address': td_address_list[count].replace('\n', '').strip(),
                    'href_map': td_href_map_list[count],
                    'working_time': td_time_list[count].replace('\n', '').strip(),
                    'brand_name': 'Мегамарт',
                    'holding_name': 'Дикси',
                    'website': 'http://www.megamart.ru',
                    'date_review': datetime.datetime.now(),
                }

                driver.get(td_href_map_list[count])
                time.sleep(6)

                print(driver.current_url)
                m = re.findall(r'@(\d+\.\d+),(\d+\.\d+)', driver.current_url)[0]
                shop['x'] = m[1]
                shop['y'] = m[0]
                all_shop.append(shop)
                count += 1
                print(f'Запись добавили {count}-count')


    def get_shops(start_page):
        table_data = start_page.find('table', class_="adrtable")
        bs_address_list = table_data.find_all('strong')
        address_list = [x.text for x in bs_address_list]
        bs_href_map_list = table_data.find_all('a')
        href_map_list = [x['href'] for x in bs_href_map_list]
        time_list = []
        for p in table_data.find_all('p'):
            if ':00' in p.text:
                time_list.append(p.text)
            else:
                pass
        return address_list, href_map_list, time_list

    start_url = 'http://www.megamart.ru/addresses.html'
    start_page = get_page(start_url)
    address_list, href_map_list, time_list = get_shops(start_page)
    get_good_data(address_list, href_map_list, time_list)
    return all_shop


def megamart_pd_data():
    """
    1. Заходим на страницу http://www.megamart.ru/addresses.html, где средствами bs4 находим таблицу с данными
       table_data = start_page.find('table', class_="adrtable")
    2. В табилце находим все
       - адреса они выделены жирным strong
       - ссылки на карты google координат как таковых на сайте нет.
       - и время работы магазина
    3. формируем 3 списка address_list, href_map_list, time_list которые для дальнейшей
       обработки передаем в get_good_data()
    4. Циклом while True: перебираяем списки забирая по индексу каждый элемент
    5. Для получения координат переходим по ссылке на google карты и помошью регулярок рапарсиваем саму ссылку
        m = re.findall(r'@(\d+\.\d+),(\d+\.\d+)', driver.current_url)[0]
        добовляем нйдееные координаты в shop = {}
    6. Записываем все магазины в all_shop = [] который возврашаем в megamart_pd_data() формируем DF
    :return:
    """
    good_data = get_data()
    df = pd.DataFrame(good_data)
    return df


