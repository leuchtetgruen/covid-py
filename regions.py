
from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os.path
import pandas as pd

CUT_OFF_DAYS = 3
LOOKBACK_DAYS = 60

NAMES = {
        '1000' : "SH",
        '2000' : "HAMBURG",
        '3000' : "NS",
        '4000' : "BREMEN",
        '5000' : "NRW",
        '6000' : "HESSEN",
        '7000' : "RLP",
        '8000' : "BW",
        '9000' : "BAYERN",
        '10000' : "SL",
        '11000' : "BERLIN",
        '12000' : "BRB",
        '13000' : "MV",
        '14000' : "SACHSEN",
        '15000' : "SA",
        '16000' : "THÜRINGEN"
        }

INHABITANTS ={
        '1000' : 2890,
        '2000' : 1890,
        '3000' : 7982,
        '4000' : 547,
        '5000' : 18000,
        '6000' : 6266,
        '7000' : 4085,
        '8000' : 11070,
        '9000' : 13080,
        '10000' : 990,
        '11000' : 3796,
        '12000' : 2520,
        '13000' : 1610,
        '14000' : 4078,
        '15000' : 2208,
        '16000' : 2137 
        }

REGIONS = ['1000',
        '2000',
        '3000',
        '4000',
        '5000',
        '6000',
        '7000',
        '8000',
        '9000',
        '10000',
        '11000',
        '12000',
        '13000',
        '14000',
        '15000',
        '16000']
col = covid.load_for_countries('rki-confirmed.csv', 'rki-deaths.csv', REGIONS)
regions = []
for region in REGIONS:
    regions.append(col.subset_for_region(region))

for region in regions:
    calculate_basics(region)
    run_interpolations(region)

fig, axs = plt.subplots(4, 4)

today = datetime.date.today() - datetime.timedelta(days=CUT_OFF_DAYS)
daysago = today - datetime.timedelta(days=LOOKBACK_DAYS)


total_weekly = ( LOOKBACK_DAYS + 1) * [0]
total_daily = ( LOOKBACK_DAYS + 1) * [0]

for i, region in enumerate(regions):
    timespan_data = region.subset_for_timespan(daysago, today)
    for idx, val in enumerate(timespan_data.values("new_infections_weekly_sum")):
        total_weekly[idx] += val

    for idx, val in enumerate(timespan_data.values("new_infection")):
        total_daily[idx] += val

total_weekly = [x / 830 for x in total_weekly]
total_daily = [x / 830 for x in total_daily]
    


for i, region in enumerate(regions):
    timespan_data = region.subset_for_timespan(daysago, today)

    region_id = region.datapoints[0].region
    row = int(i / 4)
    col = i % 4
    name = NAMES[region_id]
    inh = INHABITANTS[region_id] / 100

    weekly_adj = [x / inh for x in timespan_data.values("new_infections_weekly_sum")]
    daily_adj = [x / inh for x in timespan_data.values("new_infection")]
    ax = axs[row, col]
    ax.plot(timespan_data.dates(), weekly_adj, label="Wöchentliche Summe", color='blue')
    ax.plot(timespan_data.dates(), total_weekly, label="Dtl. Summe", color='pink', linestyle='dotted')
    ax.plot(timespan_data.dates(), daily_adj, color='lightgray', linestyle='dotted', label='Täglich')
    # ax.plot(timespan_data.dates(), total_daily, color='pink', linestyle='dotted', label='Dtl. Täglich')
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))

    if (i==0):
        ax.set_ylabel('Neuinfektionen')
        ax.legend()

    ax.set_title(name)

    # filename = "weather/{}.csv".format(region.datapoints[0].region)
    # print(filename)
    # if os.path.isfile(filename):
        # df = pd.read_csv(filename)
        # dates = pd.to_datetime(df["Datum"].array, format="%d.%m.%y")
        
        # axr = ax.twinx()
        # # axr.set_ylabel("°C")
        # # axr.plot(dates, df["max"], color="red", linestyle="dotted")
        # # axr.plot(dates, df["min"], color="blue", linestyle="dotted")

        # axr.set_ylabel("%")
        # axr.plot(dates, df["humidity"], color="green", linestyle="dotted")

        # axr.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))

plt.show()
