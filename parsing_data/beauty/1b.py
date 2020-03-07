import requests

r = requests.get('http://1b.ru/pokupatelyam/o-magazinax')
print(r.text)
# TODO c помошью re # <script>console.error