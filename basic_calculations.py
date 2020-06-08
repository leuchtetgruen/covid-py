import covid
import datetime
import numpy as np
import pdb
import math

def process_region_collection(region_collection, process_function, key, days_offset=0):
    dates = [item.date for item in region_collection.datapoints]
    for date in dates:
        item = region_collection.item_with_date(date + datetime.timedelta(days=days_offset))
        value = process_function(region_collection, date, item)
        item.remember_calculated(key, value)

    return region_collection


def calculate_daily_new_infections(region_collection):
    def calculate(region_collection, date, item):
        yesterday = date - datetime.timedelta(days=1)
        item = region_collection.item_with_date(date)
        try:
            yesterday_item = region_collection.item_with_date(yesterday)
            return item.confirmed - yesterday_item.confirmed
        except:
            return 0


    return process_region_collection(region_collection, calculate, 'new_infection')

def calculate_daily_new_deaths(region_collection):
    def calculate(region_collection, date, item):
        yesterday = date - datetime.timedelta(days=1)
        item = region_collection.item_with_date(date)
        try:
            yesterday_item = region_collection.item_with_date(yesterday)
            return item.deaths - yesterday_item.deaths
        except:
            return 0


    return process_region_collection(region_collection, calculate, 'new_deaths')

def calculate_current_r(region_collection, generation_days=4, target_key='r', source_key='new_infection'):
    def calculate(region_collection, date, item):
        recent_days = region_collection.subset_for_timespan(date - datetime.timedelta(days=generation_days-1), date)
        olden_days = region_collection.subset_for_timespan(date - datetime.timedelta(days=2*generation_days-1), date - datetime.timedelta(days=generation_days)) 
        recent_infections_sum = np.sum([x.find_calculated(source_key, 0) for x in recent_days.datapoints])
        olden_infections_sum = np.sum([x.find_calculated(source_key, 0) for x in olden_days.datapoints])

        return float(recent_infections_sum / olden_infections_sum)


    return process_region_collection(region_collection, calculate, target_key)

    
def calculate_active_cases(region_collection, infection_duration=20):
    def calculate(region_collection, date, item):
        recent_days = region_collection.subset_for_timespan(date - datetime.timedelta(days=infection_duration-1), date)
        return int(np.sum([x.find_calculated("new_infection", 0) for x in recent_days.datapoints]))

    
    return process_region_collection(region_collection, calculate, 'active_cases')

def calculate_cfr(region_collection, days_from_registration_until_death=14):
    def calculate(region_collection, date, item):
        try:
            registration_day = date - datetime.timedelta(days=days_from_registration_until_death)
            registration_day_item = region_collection.item_with_date(registration_day)
            return float(item.deaths / registration_day_item.confirmed)
        except:
            return 0

    return process_region_collection(region_collection, calculate, 'cfr')

def calculate_days_since_last_infection(region_collection):
    def calculate(region_collection, date, item):
        if item.find_calculated('new_infection') > 0:
            return 0

        d_last = region_collection.subset(lambda c: c.find_calculated('new_infection') > 0).latest_item().date
        return ( item.date - d_last ).days

    return process_region_collection(region_collection, calculate, 'days_since_last_infection')


def reduce_weekly(region_collection, source_key, target_key, average=False):
    def calculate(region_collection, date, item):
        week = date.isocalendar()[1]
        all_days_of_week = [x for x in region_collection.datapoints if x.date.isocalendar()[1] == week]
        npsum = np.sum([x.find_calculated(source_key) for x in all_days_of_week])
        if math.isnan(npsum) or math.isinf(npsum):
            thesum = 0
        else:
            thesum = int(npsum)
        theavg = float(thesum / len(all_days_of_week))

        if average:
            return theavg
        else:
            return thesum

    return process_region_collection(region_collection, calculate, target_key)

def calculate_r_weekly(region_collection):
    return reduce_weekly(region_collection, 'r', 'r_weekly', True)

def calculate_new_infections_weekly(region_collection):
    return reduce_weekly(region_collection, 'new_infection', 'new_infections_weekly', True)

def calculate_new_deaths_weekly(region_collection):
    return reduce_weekly(region_collection, 'new_deaths', 'new_deaths_weekly', True)

def calculate_basics(region_collection):
    calculate_daily_new_infections(region_collection)
    calculate_daily_new_deaths(region_collection)
    calculate_current_r(region_collection)
    calculate_current_r(region_collection, 4, 'r_deaths', 'new_deaths')
    calculate_current_r(region_collection, 7, 'r7')
    calculate_cfr(region_collection)
    calculate_active_cases(region_collection)
    calculate_days_since_last_infection(region_collection)

    calculate_r_weekly(region_collection)
    calculate_new_infections_weekly(region_collection)
    calculate_new_deaths_weekly(region_collection)
    reduce_weekly(region_collection, 'r_deaths', 'r_deaths_weekly', True)
    reduce_weekly(region_collection, 'r7', 'r7_weekly', True)
    reduce_weekly(region_collection, 'new_infection', 'new_infections_weekly_sum')

    process_region_collection(region_collection, lambda r,d,i : i.confirmed, 'confirmed')
    process_region_collection(region_collection, lambda r,d,i : i.deaths, 'deaths')

    return region_collection

def transform_to_realtime(collection, delay_in_days):
    dc = covid.DataCollection([], collection.dictionary)
    for datapoint in collection.datapoints:
        dp = datapoint.copy()
        dp.date = dp.date - datetime.timedelta(days=delay_in_days)
        dc.add_datapoint(dp)

    return dc
