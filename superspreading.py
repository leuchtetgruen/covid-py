import datetime
import pandas as pd
import numpy as np
import pdb
import covid
import basic_calculations

MONTH = 4
MIN_NI = 15
MIN_RATIO = 5
ADDITIONAL_DAYS = 3

def is_lk_data(region_id):
    return region_id.isnumeric() and (not region_id.endswith('000' ))

print("Loading data...")
PREFIX = "rki-"
data = covid.load_for_countries(PREFIX + 'confirmed.csv', PREFIX + 'deaths.csv', [], False)

print("Preparing data...")
all_regions = np.unique([x.region for x in data.datapoints])
regions = [data.subset_for_region(r) for r in all_regions]
all_calc_dps = []

print("Calculating new infections")
for region in regions:
    basic_calculations.calculate_daily_new_infections(region)
    for dp in region.datapoints:
        all_calc_dps.append(dp)


print("Finding data points in {} with at least {} new infections".format(MONTH, MIN_NI))
cluster_candidates = [x for x in all_calc_dps if (x.date.month == MONTH) and (x.find_calculated("new_infection") > MIN_NI)]
narrowed_down = []
lc = len(cluster_candidates)

print("Narrowing down to those that have {}x more infections than the day before".format(MIN_RATIO))
for i, cc in enumerate(cluster_candidates):
    if (i % 100 == 0):
        print("{} / {}".format(i, lc))

    prev_items = [x for x in all_calc_dps if ( x.date == ( cc.date - datetime.timedelta(days=1) ) ) and (x.region == cc.region)]
    if len(prev_items) == 0:
        continue

    prev_item = prev_items[0]
    new_inf_from_prev = prev_item.find_calculated("new_infection")
    cur_new_inf = cc.find_calculated("new_infection")

    if (new_inf_from_prev == 0) or ((cur_new_inf / new_inf_from_prev) > MIN_RATIO):
        narrowed_down.append(cc)

print("Identifying {} days following initial super spreading in those regions...".format(ADDITIONAL_DAYS))
days_and_regions = [[x.date, x.region] for x in narrowed_down]
ld = len(days_and_regions)
unique_days_and_regions = []

for j, day_and_region in enumerate(days_and_regions):
    if (j % 100 == 0):
        print("{} / {}".format(j, ld))

    for i in range(ADDITIONAL_DAYS):
        to_add = [day_and_region[0] + datetime.timedelta(days=i), day_and_region[1]]
        if not ( to_add in unique_days_and_regions ):
            unique_days_and_regions.append(to_add)

dc = covid.DataCollection(all_calc_dps)
new_unique = [x for x in unique_days_and_regions if is_lk_data(x[1])]
dps = [dc.item_with_date_and_region(x[0], x[1]) for x in new_unique]
dps_wo_none = [x for x in dps if not x == None]
unique_sum = np.sum([x.find_calculated("new_infection") for x in dps_wo_none])

print(unique_sum)
total_sum = np.sum([x.find_calculated("new_infection") for x in all_calc_dps if (x.date.month == MONTH) and is_lk_data(x.region)])
print(total_sum)
print("Found {} infections of {} that are related to clusters.".format(unique_sum, total_sum))

pdb.set_trace()
