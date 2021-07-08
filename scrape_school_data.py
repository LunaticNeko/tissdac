# TAKE revised table ==> append staff count if not exists, then scrape the data one by one

import pandas as pd
import numpy as np
import os
import urllib.request
from urllib.error import HTTPError
import re

FORCE_UPDATE = False

execution_start_time = pd.Timestamp.now()

# counters for received, error-4xx, error-other, error-timeout, error-value, updated, and skipped
counts = {'RECV': 0, 'E4XX': 0, 'EOTH': 0, 'ETMO': 0, 'EVAL': 0, 'UPDT': 0, 'SKIP': 0}

def format_url_teacher(school_id, area_code):
    FORMAT_STR = "https://data.bopp-obec.info/emis/schooldata-view_techer.php?School_ID={0}&Area_CODE=1017{1:02d}"
    return FORMAT_STR.format(school_id, area_code)

def save():
    df_s.to_csv(os.path.join('data', 'revised_school_table.csv'), encoding='utf_8', index=False)

df_s = pd.read_csv(os.path.join('data', 'revised_school_table.csv'), encoding='utf_8', infer_datetime_format=True)

# TABLE PREPARATION

# prepare the main table file, adding necessary columns
new_cols = ['count.principal', 'count.viceprincipal', 'count.teacher',
            'count.assistant', 'count.empperm', 'count.staff', 'count.emptemp',
            'sum.execs', 'sum.teachers']

for col in new_cols:
    if col not in df_s:
        df_s[col] = 0

if 'time.staffdataretrieved' not in df_s:
    df_s['time.staffdataretrieved'] = pd.Timestamp('1900-01-01 00:00:00')

for index, school in df_s.iterrows():
    if (not FORCE_UPDATE) and (pd.Timestamp(school['time.staffdataretrieved']) > pd.Timestamp('1900-01-01 00:00:00')):
        counts['SKIP'] += 1
        continue
    try:
        with urllib.request.urlopen(format_url_teacher(school['code.ministry'], school['old.area.code'])) as response:
            html = response.read()
            staff_table = pd.read_html(html)[-1]
            extracted_staff_count = list(map(int, np.array(staff_table.loc[(staff_table[1] == 'รวม') | (staff_table[2] == 'ครูผู้ช่วย') | ((staff_table[1] == '-') & (staff_table[2] == '-'))].iloc[:,5]).tolist()))
            extracted_staff_count += [sum(extracted_staff_count[0:2]),
                                      sum(extracted_staff_count[2:4])]
            df_s.loc[df_s['code.ministry'] == school['code.ministry'], new_cols] = extracted_staff_count
            df_s.loc[df_s['code.ministry'] == school['code.ministry'], 'time.staffdataretrieved'] = pd.Timestamp.now()
            #print(school['code.ministry'], extracted_staff_count)
            counts['RECV'] += 1
    except ValueError:
        counts['EVAL'] += 1
    except urllib.error.HTTPError:
        if 400 <= err.code <= 499:
            counts['E4XX'] += 1
        else:
            counts['EOTH'] += 1
    except TimeoutError:
        counts['ETMO'] += 1
    except urllib.error.URLError:
        counts['ETMO'] += 1

    if index%100 == 0: #autosave
        save()
        print("Saved data up to district [{0:02d}=>{1:02d}]: {2}".format(school['old.area.code'], school['new.area.code'], school['name.th']))
save()
print("All done. See below for summary of operation results:")
print(counts)
