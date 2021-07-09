import pandas as pd
import numpy as np
import os

df_s = pd.read_csv(os.path.join('data', 'school_table.csv'), encoding='utf_8')
df_a = pd.read_csv(os.path.join('refs', 'area_conversion_list.csv'), encoding='utf_8')

list_of_tuples = list(tuple(x) for x in list(df_a[['old.area.code', 'province.code', 'new.area.code']].to_numpy()))
conversion_dict = {(x,y):z for (x,y,z) in list_of_tuples}

def convert_area_code(conversion_tuple):
    (old_area, province) = conversion_tuple
    if province == 10:
        return old_area
    else:
        return conversion_dict[(old_area, province)]

df_s['conversion'] = list(zip(df_s['old.area.code'], df_s['province.code']))
df_s['new.area.code'] = df_s['conversion'].apply(convert_area_code)
df_s = df_s.drop(columns=['conversion'])
df_s = df_s.merge(df_a)
df_s.to_csv(os.path.join('data', 'revised_school_table.csv'), encoding='utf_8', index=False)
