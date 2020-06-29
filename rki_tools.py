import datetime
from collections import Counter
import itertools
import numpy as np

def for_region(arr, region_prefix):
    return [x for x in arr if str(x.region_id).zfill(5).startswith(region_prefix)]

def for_age_bracket(arr, age_bracket):
    return [x for x in arr if x.age_bracket == age_bracket]

def for_timespan(arr, d1, d2):
    return [x for x in arr if (x.date >= d1) and (x.date <= d2)]

def for_week(arr, d1):
    return for_timespan(arr, d1, d1 + datetime.timedelta(days=6))

def for_date(arr, d):
    return [x for x in arr if x.date == d]

def count_array(datapoints, property_lambda):
    return list(itertools.chain.from_iterable([x.count * [property_lambda(x)] for x in datapoints]))

def timeline(datapoints, property_lambda):
    from_date = min([x.date for x in datapoints])
    to_date = max([x.date for x in datapoints])

    print(from_date)
    print(to_date)
    data = []
    for offset in range(0, ( to_date - from_date ).days):
        date = from_date + datetime.timedelta(days=offset)
        value = np.sum([property_lambda(x) for x in datapoints if x.date == date])
        print("Appending [{}, {}]".format(date, value))
        data.append([date, value])

    return data



def RelativeCounter(values):
    counter = Counter(values)
    total_count = sum(counter.values())
    relative = {}
    for key in counter:
        relative[key] = counter[key] / total_count

    return relative

AGE_BRACKETS = ["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79", "A80+"]
REGIONS = {
        "SCHLESWIG-HOLSTEIN" : "01",
        "HAMBURG" : "02",
        "NIEDERSACHSEN": "03",
        "BREMEN" : "04",
        "NRW" : "05",
        "HESSEN" : "06",
        "RHEINLAND-PFALZ" : "07",
        "BAWUE": "08",
        "BAYERN" : "09",
        "SAARLAND" : "10",
        "BERLIN" : "11",
        "BRANDENBURG" : "12",
        "MV" : "13",
        "SACHSEN" : "14",
        "SACHSEN-ANHALT" : "15",
        "THUERINGEN" : "16",
        "GERMANY" : ""
        }


BEZIRKE = {
    "11001" : "Mitte",
    "11002" : "FH/Kreuzberg",
    "11003" : "Pankow",
    "11004" : "Charlottenburg-Wdorf",
    "11005" : "Spandau",
    "11006" : "Steglitz-Zdorf",
    "11007" : "Thof-Schöneberg",
    "11008" : "Neukölln",
    "11009" : "Treptow-Kpn",
    "11010" : "Marzahn-Hdorf",
    "11011" : "Lichtenberg",
    "11012" : "Reinickendorf"
}
