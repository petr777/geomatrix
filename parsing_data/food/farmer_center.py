import requests
import re
import json

# TODO РАЗОБРАТЬ
def get_data():
    url = "https://фермер-центр.рф/stores/"
    r = requests.get(url).text
    # ВРЕМЯ РАБОТЫ ОДНО ДЛЯ ВСЕХ
    time_work = re.findall(r"let rr = '<br/>(.*)';", r)[0]
    for row in re.findall(r"DG.marker\((.*);", r):
        # Делаем строки одинаковыми убираем иконки шариков это магазины недавно открывшиеся
        row = row.replace(', {icon: i2}', '')
        # Ставим всесто фрагмента текста ","
        row = row.replace(").addTo(map).bindPopup('", ',')
        # И убиираем ненужное окончание
        row = row.replace("'+rr)", '')
        # Забираем из строки координаты
        coord = re.findall(r"\[(.*)]", row)[0]
        x,y  = coord.split(',')
        print(x, y)
        # Удаляем координаты из строки оставляем только адрес
        address = re.sub(r"\[(.*)],",'',row)
        print(address)
        # Время работы
        time_work = time_work

get_data()

