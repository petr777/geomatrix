import pandas as pd
from pandas import ExcelWriter

from maxidom import maxidom_pd_data
from bautsentr import bautsentr_pd_data
from akson import akson_pd_data

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'xlsx\{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

data = maxidom_pd_data()
df = pd.DataFrame(data)
write_xlsx(df, 'maxidom_pd_data')