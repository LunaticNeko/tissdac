import pandas as pd
import numpy as np
import os

df_s = pd.read_csv(os.path.join('data', 'revised_school_table.csv'), encoding='utf_8')

def sorter(L):
    return dict(zip(L, range(len(L))))

#region_order = list('BCNIS')
#region_order_sorter = sorter(region_order)
#size_order = list('xlms')
#size_order_sorter = sorter(size_order)

summary_teachers_by_region = df_s.sort_values(['region', 'new.area.code', 'size']).set_index('region').groupby(['size','region'])[['sum.execs','sum.teachers']].sum().fillna(0).astype('int32')
summary_teachers_by_region.to_csv(os.path.join('reports', 'report_teachers_by_region.csv'), encoding='utf_8', index=True)

# Right part of Table 1 (teacher count by region without size discrimination)
summary_teachers = df_s.sort_values(['region', 'new.area.code']).groupby(['region', 'new.area.code'])[['sum.execs','count.teacher','count.assistant']].sum().fillna(0).astype('int32')
summary_teachers.to_csv(os.path.join('reports', 'report_teachers.csv'), encoding='utf_8', index=True)

summary_count = df_s.sort_values(['region', 'new.area.code', 'size']).groupby(['region', 'new.area.code', 'size'])[['code.ministry']].count().unstack().fillna(0).astype('int32')
summary_count.to_csv(os.path.join('reports', 'report_count.csv'), encoding='utf_8', index=True)

