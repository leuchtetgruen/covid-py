import datetime
import pandas as pd
import numpy as np
import math


def string_to_date(date_str):
    components = [int(s) for s in date_str.split("/")]
    month = components[0]
    day = components[1]
    year = 2000 + components[2]
    return datetime.date(year, month, day)

def datapoints_from_row(row):
    dps = []
    region = row['Country/Region']
    dates = row.keys().values[4:]
    for s_date in dates:
        date = string_to_date(s_date)
        dp = DataPoint(date, region)
        dp.buffer = (row[s_date])
        dps.append(dp)

    return dps

class DataCollection:
    def __init__(self, datapoints=[], dictionary={}):
        self.datapoints = datapoints.copy()
        self.dictionary = dictionary.copy() 

    def add_datapoint(self, dp):
        self.datapoints.append(dp)

    def subset(self, criteria):
        l = [x for x in self.datapoints if criteria(x)]
        return DataCollection(l, self.dictionary)

    def single_subset(self, criteria):
        try:
            return next((x for x in self.datapoints if criteria(x)))
        except:
            return None

    def item_with_date_and_region(self, date, region):
        return self.single_subset(lambda c: ( c.date == date ) and ( c.region == region ))

    def item_with_date(self, date):
        return self.single_subset(lambda c: c.date == date)

    def subset_for_region(self, region):
        return self.subset(lambda c: c.region == region).remember('region', region)

    def subset_for_timespan(self, d_from, d_to):
        return self.subset(lambda c: c.date >= d_from and c.date <= d_to)

    def dates(self):
        return  np.array([item.date for item in self.datapoints])

    def values(self,key):
        return  np.array([item.find_calculated(key) for item in self.datapoints])

    def remember(self, key, value):
        self.dictionary[key] = value
        return self

    def get(self, key):
        return self.dictionary[key]

class DataPoint:
    def __init__(self, date, region):
        self.date = date
        self.region = region

        self.confirmed = 0
        self.deaths = 0

        self.buffer = 0
        self.calculated = {}

    def remember_calculated(self, key, value):
        self.calculated[key] = value

    def find_calculated(self, key, else_value=0):
        if self.has_calculated(key):
            return self.calculated[key]
        else:
            return else_value

    def has_calculated(self, key):
        return (key in self.calculated)

    def asdict(self):
        return {
                'date': self.date,
                'region': self.region,
                'confirmed': self.confirmed,
                'deaths': self.deaths,
                'calculated' : self.calculated
                }

    def copy(self):
        dp =  DataPoint(self.date, self.region)
        dp.confirmed = self.confirmed
        dp.deaths = self.deaths
        dp.buffer = self.buffer
        dp.calculated = self.calculated

        return dp


def load_for_countries(confirmed_csv, deaths_csv, countries):
    db = DataCollection()

    df_c = pd.read_csv(confirmed_csv)
    for i, row in df_c.iterrows():
        if (row['Country/Region'] not in countries) or (type(row['Province/State']) == str):
        # if (row['Country/Region'] not in countries):
            continue

        for dp in datapoints_from_row(row):

            db.add_datapoint(dp)

    df_c = pd.read_csv(deaths_csv)
    for i, row in df_c.iterrows():
        if (row['Country/Region'] not in countries) or (type(row['Province/State']) == str):
            continue

        for dp in datapoints_from_row(row):
            dp_orig = db.item_with_date_and_region(dp.date, dp.region)
            dp_orig.deaths = dp.buffer
            dp_orig.confirmed = dp_orig.buffer


    return db
