import pandas as pd
import numpy as np
import os

df_oacl = pd.read_csv(os.path.join('data', 'school_table.csv'), usecols=["old.area.code", "province.code"], dtype={"old.area.code": str, "province.code": str})

df_oacl = pd.DataFrame(set(tuple(x) for x in list(df_oacl.to_numpy())), columns=['old.area.code', 'province.code'])

df_oacl.to_csv(os.path.join('data', 'old_area_code_list.csv'), encoding="utf_8", index=False)

