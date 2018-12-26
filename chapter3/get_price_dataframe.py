import sqlite3
import pandas as pd

def get_price_dataframe(db_file_name, code):
    conn = sqlite3.connect(db_file_name)
    return pd.read_sql('SELECT date, open, high, low, close, volume '
                       'FROM prices '
                       'WHERE code = ? '
                       'ORDER BY date',
                       conn,
                       params=(code,),
                       parse_dates=('date',),
                       index_col='date')
