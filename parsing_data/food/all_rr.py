import requests
import re
import json

# TODO РАЗОБРАТЬ JSON
r = requests.get('https://yandex.ru/map-widget/v1/?um=constructor%3A15d2d10dd4fd8c2e32f0b2b7c1f5429222bcc42b7637593686d661bbd97769e8&source=constructor').text
result = re.findall(r'provide\({"ymj":"1.0"(.*)\);', r)[0]
JSON = json.loads('{"ymj":"1.0"' + result)

for items in JSON['maps']:
    for shop in items['geoObjects']['features']:
        name = shop['properties']['name']
        address = shop['properties']['iconCaption']
        coordinates = shop['geometry']['coordinates']
        # TODO проверить
        x = coordinates[0]
        y = coordinates[1]
        print(name)
        print(address)
        print(x, y)
        print(json.dumps(shop, indent=4))