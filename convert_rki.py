import datetime
import pandas as pd
import numpy as np
import pdb
from rki import RKIDataPoint, load_rki_csv


CONVERT_HASHES = {
        1000: [1002, 1003, 1004, 1051, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062],
        3000: [3101, 3102, 3103, 3151, 3153, 3154, 3155, 3157, 3158, 3159, 3241, 3251, 3252, 3254, 3255, 3256, 3257, 3351, 3352, 3353, 3354, 3355, 3356, 3357, 3358, 3359, 3360, 3361, 3401, 3402, 3403, 3404, 3405, 3451, 3452, 3453, 3454, 3455, 3456, 3457, 3458, 3459, 3460, 3461, 3462],
        4000: [4011, 4012],
        5000: [5111, 5112, 5113, 5114, 5116, 5117, 5119, 5120, 5122, 5124, 5154, 5158, 5162, 5166, 5170, 5314, 5315, 5316, 5334, 5358, 5362, 5366, 5370, 5374, 5378, 5382, 5512, 5513, 5515, 5554, 5558, 5562, 5566, 5570, 5711, 5754, 5758, 5762, 5766, 5770, 5774, 5911, 5913, 5914, 5915, 5916, 5954, 5958, 5962, 5966, 5970, 5974, 5978],
        6000: [6411, 6412, 6413, 6414, 6431, 6432, 6433, 6434, 6435, 6436, 6437, 6438, 6439, 6440, 6531, 6532, 6533, 6534, 6535, 6611, 6631, 6632, 6633, 6634, 6635, 6636],
        7000: [7111, 7131, 7132, 7133, 7134, 7135, 7137, 7138, 7140, 7141, 7143, 7211, 7231, 7232, 7233, 7235, 7311, 7312, 7313, 7314, 7315, 7316, 7317, 7318, 7319, 7320, 7331, 7332, 7333, 7334, 7335, 7336, 7337, 7338, 7339, 7340],
        8000: [8111, 8115, 8116, 8117, 8118, 8119, 8121, 8125, 8126, 8127, 8128, 8135, 8136, 8211, 8212, 8215, 8216, 8221, 8222, 8225, 8226, 8231, 8235, 8236, 8237, 8311, 8315, 8316, 8317, 8325, 8326, 8327, 8335, 8336, 8337, 8415, 8416, 8417, 8421, 8425, 8426, 8435, 8436, 8437],
        9000: [9161, 9162, 9163, 9171, 9172, 9173, 9174, 9175, 9176, 9177, 9178, 9179, 9180, 9181, 9182, 9183, 9184, 9185, 9186, 9187, 9188, 9189, 9190, 9261, 9262, 9263, 9271, 9272, 9273, 9274, 9275, 9276, 9277, 9278, 9279, 9361, 9362, 9363, 9371, 9372, 9373, 9374, 9375, 9376, 9377, 9461, 9462, 9463, 9464, 9471, 9472, 9473, 9474, 9475, 9476, 9477, 9478, 9479, 9561, 9562, 9563, 9564, 9565, 9571, 9572, 9573, 9574, 9575, 9576, 9577, 9661, 9662, 9663, 9671, 9672, 9673, 9674, 9675, 9676, 9677, 9678, 9679, 9761, 9762, 9763, 9764, 9771, 9772, 9773, 9774, 9775, 9776, 9777, 9778, 9779, 9780],
        10000: [10041, 10042, 10043, 10044, 10045, 10046],
        11000 : [11001, 11002, 11003, 11004, 11005, 11006, 11007, 11008, 11009, 11010, 11011, 11012],
        12000: [12051, 12052, 12053, 12054, 12060, 12061, 12062, 12063, 12064, 12065, 12066, 12067, 12068, 12069, 12070, 12071, 12072, 12073],
        13000: [13003, 13004, 13071, 13072, 13073, 13074, 13075, 13076],
        14000: [14511, 14521, 14522, 14523, 14524, 14612, 14625, 14626, 14627, 14628, 14713, 14729, 14730],
        15000: [15001, 15002, 15003, 15081, 15082, 15083, 15084, 15085, 15086, 15087, 15088, 15089, 15090, 15091],
        16000: [16051, 16052, 16053, 16054, 16055, 16056, 16061, 16062, 16063, 16064, 16065, 16066, 16067, 16068, 16069, 16070, 16071, 16072, 16073, 16074, 16075, 16076, 16077]
}

rki_datapoints = load_rki_csv("./rki.csv")
print("Processing...")
min_date = min(x.date for x in rki_datapoints)
max_date = max(x.date for x in rki_datapoints)

total_days = ( max_date - min_date ).days + 2

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
