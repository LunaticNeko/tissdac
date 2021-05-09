import pandas as pd
import numpy as np
import os

df_s = pd.read_csv(os.path.join('data', 'revised_school_table.csv'), encoding='utf_8')

df_s = df_s.groupby(['region', 'new.area.code', 'size'])

summary_teachers = df_s.sum()[['number.teachers']].unstack().fillna(0).astype('int32')
summary_teachers.to_csv(os.path.join('reports', 'report_teachers.csv'), encoding='utf_8', index=True)

summary_count = df_s.count()[['code.smis']].unstack().fillna(0).astype('int32')
summary_count.to_csv(os.path.join('reports', 'report_count.csv'), encoding='utf_8', index=True)

