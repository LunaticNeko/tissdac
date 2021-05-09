import pandas as pd
import numpy as np
import os
import bisect

'''

TODO: enumerate:
school size: S/M/L/X
electricity: Y/N

'''


dfl_s = []

df_s_cols_original = pd.read_html(os.path.join("original_data", "1.xls"), skiprows=1)[1]
df_s_cols_original = df_s_cols_original.columns
df_s_cols_types = ['int', 'str', 'str', 'str', 'str',
                   'str', 'str', 'str', 'str', 'str',
                   'str', 'str', 'str', 'str', 'str',
                   'str', 'str', 'str', 'str', 'str',
                   'str', 'str', 'str', 'str', 'int',
                   'int', 'int', 'str']
conv = dict(zip(df_s_cols_original, df_s_cols_types))

for i in range(1,43):
    current_district = pd.read_html(os.path.join("original_data", str(i)+".xls"), skiprows=1)[1]
    current_district["old.area.code"] = str(i)
    dfl_s.append(current_district)

df_s = pd.concat(dfl_s, axis='index', ignore_index=True)
df_s_cols_translated = ["old.area.rank", "code.ministry", "code.smis", "code.percode", "name.th", "name.en", "principal", "class", "network", "village", "tambon", "amphoe", "province", "postcode", "email", "website", "administration", "tel", "fax", "est", "dist.toarea", "dist.toamphoe", "size", "electricity", "number.teachers", "number.students", "number.classrooms", "updated"]
df_s_cols_mapper = dict(zip(df_s_cols_original, df_s_cols_translated))
df_s = df_s.astype(conv).rename(mapper=df_s_cols_mapper, axis=1)

df_p = pd.read_csv(os.path.join('data', 'province_codes.csv'), encoding='utf_8')
df_s = df_s.merge(df_p)

# Size and Electricity Availbility Conversion
# First Priority: Based on the dataset. Otherwise:
#   Size: Classify them automatically.
#   Electricity: Assume NO.
# Both cases will generate a log report.
# Criteria Reference: TODO add reference.

size_conv = {'ขนาดเล็ก': 's',
             'ขนาดกลาง': 'm',
             'ขนาดใหญ่': 'l',
             'ขนาดใหญ่พิเศษ': 'x',
             'nan': 'n'}
elec_conv = {'มีไฟฟ้า': 'y',
             'ไม่มีไฟฟ้า': 'n'}

df_s['size'] = df_s['size'].apply(lambda x: size_conv[x])
df_s['electricity'] = df_s['electricity'].apply(lambda x: elec_conv[x])

# Code Reference (bisect function): StackOverflow::36716503
def school_size(students, size_criteria = [1, 500, 1500, 2500], size_letter = 'nsmlx'):
    return size_letter[bisect.bisect(size_criteria, students)]

# Generate a report of null values and lack of electricity
df_r1 = df_s.loc[df_s['size']=='n'].copy()
df_r1['remarks'] = 'School size classification was null.'

df_r2 = df_s.loc[df_s['electricity']=='n'].copy()
df_r2['remarks'] = 'School does not indicate access to electricity.'

df_r = pd.concat([df_r1, df_r2])

df_r.to_csv(os.path.join('reports', 'extra_reports.csv'), encoding='utf_8', index=False)

# Secondary Processing on this line
df_s.loc[df_s['size']=='n', 'size'] = list(map(school_size, df_s.loc[df_s['size']=='n', 'number.students']))


df_s.to_csv(os.path.join('data', "school_table.csv"), encoding="utf_8", index=False)

