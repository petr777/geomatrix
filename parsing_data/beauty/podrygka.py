import requests
from bs4 import BeautifulSoup

# 55.7678
# var stores
def get_page(url):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    print(page)
    return page


def get_stores_in_city(url):
    page = get_page(url)
    print(page)

def get_all_city_url():
    # Ищем все города где есть магазины
    page = get_page('https://www.podrygka.ru/shoplist/')
    all_city_url = page.find('select', class_='js-select waiting-for-style').find_all('option')
    # Приводим найденое к коректому url
    all_city_url = [x['data-control_id'] for x in all_city_url]
    bad_city_url = [x.split('_') for x in all_city_url]
    for url in bad_city_url:
        get_stores_in_city(f'https://www.podrygka.ru/shoplist/?{url[0]}_{url[1]}={url[2]}&set_filter=y')


get_all_city_url()