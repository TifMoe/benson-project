import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.ndimage.interpolation import shift
from collections import defaultdict


start17 = datetime(2017, 7, 1)
start16 = datetime(2016, 7, 2)


def datelist(startdate):
    week_list = [startdate + ((timedelta(days=-7))*i) for i in range(14)]
    clean_weeks = [i.strftime('%y%m%d') for i in week_list]
    return clean_weeks


weeks_to_import = datelist(start17) + datelist(start16)


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

# Pickle all turnstile data
final.to_pickle('raw_turnstile_data.pkl')


df = final.rename(columns=lambda x: x.strip().lower())

df['datetime'] = df['date'] + ' ' + df['time']
df['datetime_clean'] = [datetime.strptime(x, '%m/%d/%Y %H:%M:%S') for x in df['datetime']]

df.sort_values(['scp','station','c/a','unit','datetime_clean'], inplace=True)
df.reset_index(drop=True)


def find_diff_prev_row(df_series_col):
    col_array = np.array(df_series_col)
    col_array_shifted = shift(col_array, 1, cval=np.NaN)
    col_diff = col_array - col_array_shifted

    return col_diff


df['entries_diff'] = find_diff_prev_row(df['entries'])
df['exit_diff'] = find_diff_prev_row(df['exits'])

df['year'] = [x.year for x in df['datetime_clean']]

df['group_id'] = df['c/a'].astype(str) + df['unit'].astype(str) + df['scp'].astype(str) + \
                 df['station'].astype(str)  + df['year'].astype(str)

groups = set(df['group_id'])


def groups_dict(groups):
    group_dict = defaultdict(int)
    for i in enumerate(list(groups)):
        group_dict[i[1]]= i[0]

    return group_dict

group_id_dict = groups_dict(groups)

df['group_id_num'] = [group_id_dict[x] for x in df['group_id']]


def find_first_rows_groups(df_series_col):
    col_array = np.array(df_series_col)
    col_array_shifted = shift(col_array, 1, cval=np.NaN)
    first_row_mask = col_array != col_array_shifted

    return first_row_mask


df['first_row_group'] = find_first_rows_groups(df['group_id_num'])


# Make entries_diff and exit_diff nan when first row in group or negative value
df.loc[df['first_row_group'], 'entries_diff'] = None
df.loc[df['entries_diff'] < 0, 'entires_diff'] = None

df.loc[df['first_row_group'], 'exit_diff'] = None
df.loc[df['exit_diff'] < 0, 'exit_diff'] = None

df.to_pickle('final_turnstile_data.pkl')
