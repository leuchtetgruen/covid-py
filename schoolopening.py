import datetime
import pandas as pd
import numpy as np
import pdb
from rki import RKIDataPoint, load_rki_csv
from rki_tools import for_region, for_age_bracket, for_timespan, for_week, AGE_BRACKETS, REGIONS

data = load_rki_csv("./rki.csv")

WEEKS = [datetime.date(2020, 4, 27), datetime.date(2020, 5, 4), datetime.date(2020, 5, 11), datetime.date(2020, 5, 18), datetime.date(2020, 5, 25)]
MY_REGIONS = [
    'NIEDERSACHSEN',
    'NRW',
    'HESSEN',
    'RHEINLAND-PFALZ',
    'BAWUE',
    'BAYERN',
    'BERLIN',
    'BRANDENBURG'
]
MY_AGE_BRACKETS = ['A05-A14', 'A60-A79']

for week in WEEKS:
    print("Für die Woche ab {}".format(week))
    for ab in MY_AGE_BRACKETS:
        print(" Altersgruppe {}".format(ab))
        for region in MY_REGIONS:
            region_id = REGIONS[region]
            cases = np.sum([x.count for x in for_week(for_age_bracket(for_region(data, region_id), ab), week)])
            print("  In {}: {}".format(region, cases))

    print("")
