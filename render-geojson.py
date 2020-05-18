from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import datetime
import json
import numpy as np
import pdb
import math

# REFERENCE_DATE = datetime.date(2020, 5, 6)
# OUTPUT_FILENAME = "{}-r_weekly.geojson".format(str(REFERENCE_DATE.year) + "-" + str(REFERENCE_DATE.month) + "-" + str(REFERENCE_DATE.day))

def add_to_dataset(collection, date, dataset):
    item = collection.item_with_date(date)

    if (item == None):
        return

    for key in item.calculated.keys():
        v = item.calculated[key]
        if math.isnan(v):
            dataset[key] = -10000
        elif math.isinf(v):
            dataset[key] = -20000
        else:
            dataset[key] = v

def create_json_for_day(date):
    output_filename = "{}.geojson".format(str(date.year) + "-" + str(date.month) + "-" + str(date.day))

    for dataset in geo_json_data:
        if (not 'cca_2' in dataset):
            continue

        region_id = dataset['cca_2'].lstrip("0")
        region_collection = [x for x in regions_list if x.get('region') == region_id][0]
        print(region_id)
        add_to_dataset(region_collection, date, dataset)
        print(dataset)

    with open(output_filename, 'w') as output_file:
        json.dump(geo_json, output_file)

        output_file.close()
    

with open('./landkreise.json') as json_file:
    geo_json = json.load(json_file)

geo_json_data = [x['properties'] for x in geo_json['features']]
regions = [x['cca_2'].lstrip("0") for x in geo_json_data if 'cca_2' in x]

print("Loading for {} regions...".format(len(regions)))
all_rki_data = covid.load_for_countries("./rki-confirmed.csv", "./rki-deaths.csv", regions)

regions_list = []
for region in regions:
    regions_list.append(all_rki_data.subset_for_region(str(region)).remember('region', region))

for region_dc in regions_list:
    calculate_basics(region_dc)
    run_interpolations(region_dc)

# for dataset in geo_json_data:
    # if (not 'cca_2' in dataset):
        # continue

    # region_id = dataset['cca_2'].lstrip("0")
    # region_collection = [x for x in regions_list if x.get('region') == region_id][0]
    # print(region_id)
    # add_to_dataset(region_collection, REFERENCE_DATE, dataset)
    # print(dataset)

# with open(OUTPUT_FILENAME, 'w') as output_file:
    # json.dump(geo_json, output_file)

    # output_file.close()

print("run create_json_for_day(datetime.date(yyyy, mm, dd)) in order to create json file")

pdb.set_trace()
