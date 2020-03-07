import requests
import re

# Todo нет городов может прокатит но лутше сделать хорошо
def get_data():
    r = requests.get('https://www.ugdvor.ru/allshop/')
    r = r.text.replace('\n', '').replace('\n', '')
    result = re.findall(r"    DG.marker(.*?)</span>'\);", r)
    for store in result:
        print(store)

get_data()