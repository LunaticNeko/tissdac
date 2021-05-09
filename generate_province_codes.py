import pandas as pd
import numpy as np
import os

dc_cols = ["pc.bot", "province", "province.code", "dc.bot", "dn", "dc"]
df_dc = pd.read_excel(os.path.join('refs', "district_codes.xls"), sheet_name="map รหัสอำเภอ_กรมการปกครอง", skiprows=4)
dc_col_map = dict(zip(df_dc.columns, dc_cols))
df_dc = df_dc.rename(dc_col_map, axis='columns').dropna().drop(["pc.bot", "dc.bot", "dn", "dc"], axis='columns')

# convert to string and keep only first 2 letters (the MOI province code we need)
df_dc['province.code'] = df_dc['province.code'].astype('string').apply(lambda x: x[:2])
# remove the word "จังหวัด"
df_dc['province'] = df_dc['province'].apply(lambda x: x.replace('จังหวัด', ''))

df_dc.to_csv(os.path.join('data', "province_codes.csv"), encoding="utf_8", index=False)

