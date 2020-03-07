import requests
import re

# TODO нужен selenium
def get_data():
    r = requests.get('https://goldapple.ru/stockists')
    print(r.text)

get_data()