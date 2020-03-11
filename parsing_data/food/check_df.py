import pandas as pd
from pandas import ExcelWriter

from all_rr import all_rr_pd_data
from europa_ts import europa_ts_pd_data
from fermer_center import fermer_center_pd_data
from miratorg import miratorg_pd_data
from myfasol import myfasol_pd_data
from samberi import samberi_pd_data
from slata import slata_pd_data
from zao_agrokomplex import agro_kompleks_pd_data


def write_xlsx(df, name_file):
    writer = ExcelWriter(f'xlsx\{name_file}.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    return 'ФАЙЛ СОХРАНЕН'

data = agro_kompleks_pd_data()
df = pd.DataFrame(data)
write_xlsx(df, 'agro_kompleks_pd_data')