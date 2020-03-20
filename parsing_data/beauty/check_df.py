import pandas as pd
from pandas import ExcelWriter

from podrygka import podrygka_pd_data
from r_ulybka import r_ulybka_pd_data
from rubl_bum import rubl_bum_pd_data
from ugdvor import ugdvor_pd_data
#from goldapple import goldapple_pd_data
from iledebeaute import iledebeaute_pd_data
from sephora import sephora_pd_data
from letu import letu_pd_data
from rivegauche import rivegauche_pd_data
from yves_rocher import yves_pd_data

def write_xlsx(df, name_file):
    writer = ExcelWriter(f'xlsx\{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

data = yves_pd_data()
df = pd.DataFrame(data)
write_xlsx(df, 'yves_pd_data_new')