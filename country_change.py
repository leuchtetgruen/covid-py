from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys

COUNTRY = sys.argv[1]
date_components = [int(i) for i in sys.argv[2].split(".")]
START_DATE = datetime.date(date_components[2], date_components[1], date_components[0])


region = covid.load_for_countries('confirmed.csv', 'deaths.csv', [COUNTRY])
calculate_basics(region)
run_interpolations(region)

for N_WEEKS in range(1, 6):
    END_DATE = START_DATE + datetime.timedelta(weeks=N_WEEKS)
    startDataPoint = region.item_with_date(START_DATE)
    endDataPoint = region.item_with_date(END_DATE)

    sdWeekly = startDataPoint.find_calculated("new_infections_weekly")
    edWeekly = endDataPoint.find_calculated("new_infections_weekly")
    ratio = edWeekly / sdWeekly
    print(str(N_WEEKS) + " after imposing 2nd lockdown...")
    print(str(START_DATE) + " : " + str(sdWeekly) + " cases / week")
    print(str(END_DATE) + " : " + str(edWeekly) + " cases / week")
    print(ratio)
    print("")
