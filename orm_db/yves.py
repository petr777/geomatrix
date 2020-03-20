import pandas as pd

file = 'yves_pd_data_new.xlsx'

df = pd.read_excel(file, index_col=0)
print(df.dtypes)