import requests
import re
import json

# TODO Переписать на aio
def get_id_session(s):
    r = s.get('https://www.letu.ru/stores?')
    result = re.findall(r"sessionStorage.setItem\('_dynSessConf',(.*)\);", r.text)[0]
    result = result.replace("'","").strip()
    return result

def get_all_city_id():
    s = requests.Session()
    id_session = get_id_session(s)
    all_city = []
    for id_city in range(60000, 80000):
        url = f"https://www.letu.ru/rest/model/atg/rest/geolocation/actor/GeolocationActor/setGeolocationInfo?pushSite=storeMobileRU&locale=ru_RU&cityId={id_city}&pushSite=storeMobileRU&_dynSessConf={id_session}"
        resp = s.get(url)
        JSON = json.loads(resp.text)
        result = JSON['result']
        city = {
            'id': id_city,
            'name': result['name']
        }
        print(city)
        all_city.append(city)
    return all_city

all_city = get_all_city_id()
print(all_city)
f = open("all_city3.txt", "w")
for item in all_city:
    f.write(f"{item}\n")
