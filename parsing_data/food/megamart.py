import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_data():
    driver = webdriver.Chrome()
    def get_good_data(td_address_list, td_href_map_list, td_time_list):
        newList = []
        count = 0
        sizeOfList = len(td_address_list)
        while True:
            shop = {
                'address': td_address_list[count],
                'href_map': td_href_map_list[count],
                'working_time': td_time_list[count],
            }
            print(shop['address'])
            driver.get(td_href_map_list[count])
            time.sleep(7)
            print(driver.current_url)
            m = re.findall(r'@(\d+\.\d+),(\d+\.\d+)', driver.current_url)[0]
            print(m)
            newList.append(shop)
            count += 1
            if count == sizeOfList:
                break
        return newList

    def get_data(start_page):
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
    address_list, href_map_list, time_list = get_data(start_page)
    good_data = get_good_data(address_list, href_map_list, time_list)
    print(good_data)


get_data()
"""# TODO нужно перейти по каждой ссылке google скорее всего понадобится selenium выдрать текуший url после переадресации
# TODO в нем координаты
for row in good_data:
    url = row['href_map']
    print(url)
    page = get_page(url)
    print(page.title.text)
    print(page)"""