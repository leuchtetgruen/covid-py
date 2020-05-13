from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import datetime
import json
import numpy as np
import pdb
import math

KEY_TO_TRANSFER = 'r'
OUTPUT_FILENAME = "2020-05-13-r.geojson"

def defer_value(collection, key, default=0):
    start_day = datetime.date.today() - datetime.timedelta(days=3)
    subset = collection.subset(lambda x: x.date >= start_day)
    print(len(subset.datapoints))
    if len(subset.datapoints) > 0:
        val = np.average(subset.values(key))
        if math.isnan(val) or math.isinf(val):
            return default
        else:
            return val
    else:
        return default
    

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

for dataset in geo_json_data:
    if (not 'cca_2' in dataset):
        continue

    region_id = dataset['cca_2'].lstrip("0")
    region_collection = [x for x in regions_list if x.get('region') == region_id][0]
    print(region_id)
    val = defer_value(region_collection, KEY_TO_TRANSFER, -1)
    dataset[KEY_TO_TRANSFER] = val
    print(val)

with open(OUTPUT_FILENAME, 'w') as output_file:
    json.dump(geo_json, output_file)

    output_file.close()

