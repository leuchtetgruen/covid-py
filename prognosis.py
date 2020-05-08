import math
import datetime
import numpy as np
import basic_calculations
from covid import DataCollection, DataPoint

def create_timeline_with_r(base_data, start_date, days, r=0, generation_days=4):

    dc = DataCollection(base_data.datapoints)
    for offset in range(1, days):
        date = start_date + datetime.timedelta(days=offset)

        old_dp = dc.item_with_date(date - datetime.timedelta(days=generation_days))
        new_infection = old_dp.find_calculated("new_infection") * r
        yesterday = dc.item_with_date(date - datetime.timedelta(days=1))

        dp = DataPoint(date, dc.datapoints[0].region)
        dp.confirmed = yesterday.confirmed + new_infection
        dp.remember_calculated("confirmed", dp.confirmed)
        dp.remember_calculated("new_infection", new_infection
                )
        dp.remember_calculated("r", r)

        dc.add_datapoint(dp)


    basic_calculations.calculate_basics(dc)
    return dc.subset_for_timespan(start_date, start_date + datetime.timedelta(days=days))



