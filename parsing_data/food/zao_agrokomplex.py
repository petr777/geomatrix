import requests
import json

# TODO РАЗОБРАТЬ JSON
def get_data():
    url = 'https://www.zao-agrokomplex.ru/local/ajax/shops.php?type=json'
    # ЧТО ТО РУГАЕТСЯ НА SLL ВЫКЛЮЧАЕМ
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url,  verify=False).json()
    print(r)

get_data()
