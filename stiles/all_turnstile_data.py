import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.ndimage.interpolation import shift

filename = 'https://web.mta.info/developers/data/nyct/turnstile/turnstile_'+week+'.txt'

start17 = datetime(2017, 7, 1)
start16 = datetime(2016, 7, 2)


def get_week_list(startdate):
    week_list = [startdate + ((timedelta(days=-7))*i) for i in range(14)]
    clean_weeks = [i.strftime('%y%m%d') for i in week_list]
    return clean_weeks


weeks_to_import = get_week_list(start17) + get_week_list(start16)


def loadturndata(date):
    strdate = str(date)
    filename = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'+strdate+'.txt'
    df = pd.read_csv(filename)
    return df


def loadturnlist(dates):
    data = pd.DataFrame()
    x = []
    for i in dates:
        df = (loadturndata(i))
        x.append(df)
    data = pd.concat(x)
    return data


final = loadturnlist(weeks_to_import)
df = final.rename(columns=lambda x: x.strip().lower())

df['datetime'] = df['date'] + ' ' + df['time']
df['datetime_clean'] = [datetime.strptime(x, '%m/%d/%Y %H:%M:%S') for x in df['datetime']]


def find_diff_prev_row(df_series_col):
    col_array = np.array(df_series_col)
    col_array_shifted = shift(col_array, 1, cval=np.NaN)
    col_diff = col_array - col_array_shifted

    return col_diff

df['entries_diff'] = find_diff_prev_row(df['entries'])
df['exit_diff'] = find_diff_prev_row(df['exits'])

