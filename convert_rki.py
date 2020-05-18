import datetime
import pandas as pd
import numpy as np
import pdb
from rki import RKIDataPoint, load_rki_csv


CONVERT_HASHES = {
        11000 : [11001, 11002, 11003, 11004, 11005, 11006, 11007, 11008, 11009, 11010, 11011, 11012]
}

rki_datapoints = load_rki_csv("./rki.csv")
print("Processing...")
min_date = min(x.date for x in rki_datapoints)
max_date = max(x.date for x in rki_datapoints)

total_days = ( max_date - min_date ).days + 1

print("for regions...")
regions_hash = {}
for i in range(0, total_days):
    date = min_date + datetime.timedelta(days=i)
    print("Processing for date {}".format(date))
    data_for_day = [x for x in rki_datapoints if x.date == date]
    lks = np.array([x.region_id for x in data_for_day])
    uniq_lks = np.unique(lks)
    for region_id in uniq_lks:
        if not region_id in regions_hash:
            regions_hash[region_id] = {}

        new_inf = np.sum([x.count for x in data_for_day if x.region_id == region_id])
        new_dth = np.sum([x.death_count for x in data_for_day if x.region_id == region_id])
        regions_hash[region_id][date] = [new_inf, new_dth]

print("for age brackets...")
age_hash = {}
for i in range(0, total_days):
    date = min_date + datetime.timedelta(days=i)
    print("Processing for date {}".format(date))
    data_for_day = [x for x in rki_datapoints if x.date == date]
    ages = np.array([x.age_bracket for x in data_for_day])
    uniq_ages = np.unique(ages)
    for age_bracket in uniq_ages:
        if not age_bracket in age_hash:
            age_hash[age_bracket] = {}

        new_inf = np.sum([x.count for x in data_for_day if x.age_bracket == age_bracket])
        new_dth = np.sum([x.death_count for x in data_for_day if x.age_bracket == age_bracket])
        age_hash[age_bracket][date] = [new_inf, new_dth]

print("Sorting by date...")
date_hash = {}
counter = {}
for i in range(0, total_days):
    date = min_date + datetime.timedelta(days=i)
    date_hash[date] = {}
    for region_id in regions_hash.keys():
        if region_id in counter:
            ctr = counter[region_id]
        else:
            ctr = [0, 0]
        if date in regions_hash[region_id]:
            ctr[0] = ctr[0] + regions_hash[region_id][date][0]
            ctr[1] = ctr[1] + regions_hash[region_id][date][1]

        date_hash[date][region_id] = ctr.copy()
        counter[region_id] = ctr.copy()

    for age_bracket in age_hash.keys():
        if age_bracket in counter:
            ctr = counter[age_bracket]
        else:
            ctr = [0, 0]
        if date in age_hash[age_bracket]:
            ctr[0] = ctr[0] + age_hash[age_bracket][date][0]
            ctr[1] = ctr[1] + age_hash[age_bracket][date][1]

        date_hash[date][age_bracket] = ctr.copy()
        counter[age_bracket] = ctr.copy()

print("Creating sums...")
for i in range(0, total_days):
    date = min_date + datetime.timedelta(days=i)
    for key in CONVERT_HASHES.keys(): 
        ctr = [0,0]
        for s_key in CONVERT_HASHES[key]:
            # pdb.set_trace()
            s_ctr = date_hash[date][s_key]
            ctr[0] = ctr[0] + s_ctr[0]
            ctr[1] = ctr[1] + s_ctr[1]

        date_hash[date][key] = ctr



n_entries = len(list(date_hash.values())[0])
dates = [min_date + datetime.timedelta(days=i) for i in range(0, total_days)]
table_hash = {
        'Province/State': [""] * n_entries,
        'Country/Region': list(list(date_hash.values())[0].keys()),
        'Lat': [0.0] * n_entries,
        'Lon': [0.0] * n_entries
        }

table_confirmed = table_hash.copy()
table_deaths = table_hash.copy()
for date in dates:
    s_date = "{}/{}/{}".format(date.month, date.day, date.year - 2000)
    table_confirmed[s_date] = [x[0] for x in date_hash[date].values()]
    table_deaths[s_date] = [x[1] for x in date_hash[date].values()]

df_c = pd.DataFrame(table_confirmed, columns=table_confirmed.keys())
df_d = pd.DataFrame(table_deaths, columns=table_deaths.keys())

df_c.to_csv (r'rki-confirmed.csv', index = False, header=True)
df_d.to_csv (r'rki-deaths.csv', index = False, header=True)
