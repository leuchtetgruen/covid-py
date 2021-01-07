from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys


def per_100k_inhabitants(values, mio_inhabitants):
    return [( x / (mio_inhabitants * 1000000) * 100000 ) for x in values]

def add_events(events, collection, key, ax):
    for date in events.keys():
        item = collection.item_with_date(date)

        if item == None:
            continue

        value = item.find_calculated(key)
        annot = events[date]

        offset = 20
        if annot.startswith("U-"):
            offset = -20
            annot = annot.replace("U-", "")

        if annot.startswith("0-"):
            offset = 5
            annot = annot.replace("0-", "")

        ax.plot(date, value, 'b*')
        ax.annotate(annot, (mdates.date2num(date), value), xytext=(0, offset), textcoords='offset points', arrowprops=dict(arrowstyle='->'), color='blue')

regions = []

INHABITANTS = {
        "germany": 80,
        "italy" : 60,
        "sweden": 10,
        "us": 328,
        "united kingdom": 66,
        "denmark": 5,
        "norway": 5,
        "france": 67,
        "spain": 47,
        "ireland": 5,
        "poland": 40,
        "austria": 9,
        "switzerland": 8.5,
        "belgium": 11.5,
        "netherlands": 17,
        "czechia": 10.5,
        "portugal": 10
        }
SELECTED_INDEX = 0
if len(sys.argv) > 1:
    COUNTRY = sys.argv[1]
else:
    COUNTRY = "Germany"


col = covid.load_for_countries('confirmed.csv', 'deaths.csv', [COUNTRY])
regions.append(col.subset_for_region(COUNTRY).remember('mio_inhabitants', INHABITANTS[COUNTRY.lower()]))
CUT_OFF_DAYS = 3

for region in regions:
    print("Calculating for " + region.datapoints[0].region)
    calculate_basics(region)
    run_interpolations(region)


INFECTION_TO_STATISTICS_DELAY = 8
INFECTION_TO_DEATH_STATISTICS_DELAY = 20
R_DELAY = 12
LOOKBACK_DAYS = 190
ctr = regions[SELECTED_INDEX]
ctr_name = ctr.datapoints[0].region

today = datetime.date.today() - datetime.timedelta(days=CUT_OFF_DAYS)
daysago = today - datetime.timedelta(days=LOOKBACK_DAYS)
ctr_timespan = ctr.subset_for_timespan(daysago, today)

regions_timespan = [x.subset_for_timespan(daysago, today) for x in regions]

fig, axs = plt.subplots(3, 2)



# axs[0,0].plot(ctr_timespan.dates(), per_100k_inhabitants(ctr_timespan.values("active_cases"), ctr_timespan.get("mio_inhabitants")), label="Aktive Fälle")
axs[0,0].plot(ctr_timespan.dates(), ctr_timespan.values("active_cases"), label="Aktive Fälle")
axs[0,0].legend()
# axs[0,0].set_title("Aktive Fälle  / 100k EW ({})".format(ctr_name))
axs[0,0].set_title("Aktive Fälle ({})".format(ctr_name))

axs[0,1].plot(ctr_timespan.dates(), ctr_timespan.values("new_infections_weekly"), label='Wöchentlich gemittelt')
axs[0,1].plot(ctr_timespan.dates(), ctr_timespan.values("new_infections_weekly_sum"), label='Wöchentlich summiert')
axs[0,1].plot(ctr_timespan.dates(), ctr_timespan.values("new_infection"), color='lightgray', linestyle='dotted', label='Täglich')
axs[0,1].legend()
axs[0,1].set_title("Gemeldete Neuinfektionen ({})".format(ctr_name))

axs[1,0].plot(ctr_timespan.dates(), ctr_timespan.values("new_deaths_weekly"), label='Wöchentlich summiert')
axs[1,0].plot(ctr_timespan.dates(), ctr_timespan.values("new_deaths"), color='lightgray', linestyle='dotted', label='Täglich')
axs[1,0].legend()
axs[1,0].set_title("Gemeldete Todesfälle ({})".format(ctr_name))

axs[1,1].plot(ctr_timespan.dates(), ctr_timespan.values("r_weekly"), label='Wöchentlich gemittelt')
axs[1,1].plot(ctr_timespan.dates(), ctr_timespan.values("r"), color='lightgray', linestyle='dotted', label='Täglich')
axs[1,1].plot(ctr_timespan.dates(), ctr_timespan.values("r7"), color='pink',  linestyle='dotted', label='R7 (tgl)')
axs[1,1].plot(ctr_timespan.dates(), ctr_timespan.values("r7_weekly"), color='pink',  label='R7 (wöchentlich)')
axs[1,1].plot(ctr_timespan.dates(), [1] * len(ctr_timespan.dates()), color='red', linestyle='dashed', linewidth=0.5, label='R=1')
axs[1,1].legend()
axs[1,1].set_title("Entwicklung von R ({})".format(ctr_name))

dp100k = per_100k_inhabitants(ctr_timespan.values("new_deaths_weekly"), ctr.get("mio_inhabitants")) 
axs[2,0].plot(ctr_timespan.dates(), dp100k, color='pink', label='Tote / 100k Einwohner in 7 Tagen')
axs[2,0].legend()
axs[2,0].set_title("7-Tage Todesfälle / 100k EW ({})".format(ctr.get("region")))


p100k = per_100k_inhabitants(ctr_timespan.values("new_infections_weekly_sum"), ctr.get("mio_inhabitants")) 
axs[2,1].plot(ctr_timespan.dates(), p100k, color='lightblue', label='Neuinfektionen / 100k Einwohner in 7 Tagen')
axs[2,1].legend()
axs[2,1].set_title("7-Tage Inzidenz ({})".format(ctr.get("region")))
        
plt.show()

