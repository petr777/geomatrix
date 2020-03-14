import asyncio
from aiohttp import ClientSession
import pandas as pd
from pandas import ExcelWriter
import datetime
import requests
import json
from bs4 import BeautifulSoup



def get_data():
    good_data = []

    # --------------- ПОЛУЧАЕМ ДАННЫЕ ПО ОФИСАМ ---------------------#

    def cleaner_data_department(row):
        good_row = {}
        good_row['address'] = row['full_address']
        good_row['country'] = 'Russian Federation'
        good_row['name'] = row['ps_name']
        good_row['type'] = 'department'
        good_row['working_time_cash'] = str(row['work_times']['cash']).replace('[', '').replace("'", '').replace("]", '')
        good_row['working_time_fl'] = str(row['work_times']['fl']).replace('[', '').replace("'", '').replace("]", '')
        good_row['working_time_ur'] = str(row['work_times']['ur']).replace('[', '').replace("'", '').replace("]", '')
        good_row['x'] = row['longitude']
        good_row['y'] = row['latitude']
        good_row['brand_name'] = 'Росбанк'
        good_row['holding_name'] = 'Societe Generale'
        good_row['website'] = 'https://www.rosbank.ru'
        good_row['date_review'] = datetime.datetime.now()
        print(good_row)
        good_data.append(good_row)

    def get_department():
        r = requests.get('https://www.rosbank.ru/otdeleniya/')
        page = BeautifulSoup(r.text, 'html.parser')
        data = page.find('script', id="__NEXT_DATA__").text
        JSON = json.loads(data)
        for department in JSON['props']['initialState']['department']['list']:
            id_department = department['id']
            r = requests.get(f'https://api.rosbank.ru/exchange/department/list/get?id[]={id_department}&').json()
            row = r['data'][0]
            cleaner_data_department(row)

    get_department()

    # --------------- ПОЛУЧАЕМ ДАННЫЕ ПО БАНКОМАТАМ ---------------------#

    def cleaner_data_atm(row):
        good_row = {}
        good_row['address'] = row['full_address']
        good_row['city'] = row['city_name']
        good_row['country'] = 'Russian Federation'
        good_row['name'] = row['title']
        good_row['type'] = 'atm'
        good_row['code_bank'] = row['bank']
        good_row['working_time'] = row['work_mode']
        good_row['x'] = row['coords_longitude']
        good_row['y'] = row['coords_latitude']
        good_row['brand_name'] = 'Росбанк'
        good_row['holding_name'] = 'Societe Generale'
        good_row['website'] = 'https://www.rosbank.ru'
        good_row['date_review'] = datetime.datetime.now()
        print(good_row)
        good_data.append(good_row)


    async def fetch(url, session):
        headers = {'User-Agent:': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        async with session.get(url, headers=headers) as response:
            print(url)
            if response.status == 404:
                pass
            elif response.status == 200:
                row = await response.json()
                row = row['data'][0]
                cleaner_data_atm(row)

    async def bound_fetch(sem, url, session):
        async with sem:
            await fetch(url, session)

    async def run():
        tasks = []
        sem = asyncio.Semaphore(30)
        async with ClientSession() as session:
            for i in range(0, 120000):
                url = f'https://api.rosbank.ru/exchange/atm/list/get?id={i}'
                task = asyncio.ensure_future(bound_fetch(sem, url, session))
                tasks.append(task)
            responses = asyncio.gather(*tasks)
            await responses

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())
    loop.run_until_complete(asyncio.sleep(1.5))
    loop.run_until_complete(future)

    return good_data


# Функция для записи в XLSX не вызываетя ( закомпилирована ) см. maria_pd_data
def write_xlsx(df, name_file):
    writer = ExcelWriter(f'{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

def rosbank_pd_data():
    """
    1. в функции get_data() сначала получаем данные по всем офисам
        1.1 отправлем запрос по url 'https://www.rosbank.ru/otdeleniya/
        1.2 средствами bs4 находим фрагмент page.find('script', id="__NEXT_DATA__").text
        1.3 преобразуем в JSON добираемся до списка с id офисов JSON['props']['initialState']['department']['list']
        1.4 Отправляем запрос по url
            r = requests.get(f'https://api.rosbank.ru/exchange/department/list/get?id[]={id_department}&').json()
        1.5 В ответ приходит даннные по конкретному офису
        1.6 Отпавляем их в функцию cleaner_data_department(row)
        1.7 Записывае нужные данные в good_data = []

    2. Спомошью aiohttp тправляем запросы  f'https://api.rosbank.ru/exchange/atm/list/get?id={i}'
        2.1 если банкомата с таки id нет то ответ 404
        2.2 если есть то 200 и в ответ приходит json
        2.3 Отпавляем их в функцию cleaner_data_atm()
        2.4 Записывае нужные данные в good_data = []

    3. Возврашаем good_data
    4. Формируем DF

    :return:
    """

    good_data = get_data()
    df = pd.DataFrame(good_data)
    write_xlsx(df, 'rosbank')
    return df

rosbank_pd_data()