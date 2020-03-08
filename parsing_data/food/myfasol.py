import requests
import re
import json


# TODO разобрать JSON
def get_page(url):
    r = requests.get(url).text
    result = re.findall(r"shops:(.*),", r)[0]
    JSON = json.loads(result)
    return JSON

get_page('https://myfasol.ru/stores/')
