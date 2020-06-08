import datetime

def for_region(arr, region_prefix):
    return [x for x in arr if str(x.region_id).zfill(5).startswith(region_prefix)]

def for_age_bracket(arr, age_bracket):
    return [x for x in arr if x.age_bracket == age_bracket]

def for_timespan(arr, d1, d2):
    return [x for x in arr if (x.date >= d1) and (x.date <= d2)]

def for_week(arr, d1):
    return for_timespan(arr, d1, d1 + datetime.timedelta(days=6))

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
        "THUERINGEN" : "16"
        }
