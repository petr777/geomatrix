import pandas as pd


def df_to_xlsx(file):
    df = pd.read_excel('file', index_col=0)
    return df