import datetime
import pandas as pd
import numpy as np
import matplotlib as plt
from rki import RKIDataPoint, load_rki_csv
from rki_tools import for_region, for_age_bracket, for_timespan, for_week, AGE_BRACKETS, REGIONS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


data = load_rki_csv("./rki.csv")
week = datetime.date(2020, 6, 1)
all_for_week = for_week(data, week)

for region_name in REGIONS:
    print(region_name)
    all_for_region = for_region(all_for_week, REGIONS[region_name])
    total = np.sum([x.count for x in all_for_region])
    for bracket in AGE_BRACKETS:
        all_for_age_bracket_in_region = for_age_bracket(all_for_region, bracket)
        bracket_sum = np.sum([x.count for x in all_for_age_bracket_in_region])
        print(" {} : {} ({} %)".format(bracket, bracket_sum, int(bracket_sum / total * 100.0)))


