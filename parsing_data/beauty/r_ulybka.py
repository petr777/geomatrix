import requests

def get_data():
    all_stores = []
    def get_all_stores(url):
        data = requests.get(url).json()
        all_stores = data['_embedded']['items']
        for store in all_stores:
            # TODO  разобрать в all_stores
            print(store)
            all_stores.append(store)
        return data
    # Делаем запросы по url выстатвии limit 100 одним запросом не отдает более 1000 поэтому перебираем странички
    limit = 100
    for num_page in range(1, 13):
        url = f'https://delivery.shop.api.svs.tdera.ru/stores?limit={limit}&page={num_page}'
        start_page = get_all_stores(url)

