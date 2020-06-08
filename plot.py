from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


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

PREFIX = "rki-"
LK_ID = "11000"
col = covid.load_for_countries(PREFIX + 'confirmed.csv', PREFIX + 'deaths.csv', [LK_ID, 'A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 'A80+'])
regions.append(col.subset_for_region(LK_ID).remember('mio_inhabitants', 5))
regions.append(col.subset_for_region('A00-A04').remember('mio_inhabitants', 5))
regions.append(col.subset_for_region('A05-A14').remember('mio_inhabitants', 5))
regions.append(col.subset_for_region('A15-A34').remember('mio_inhabitants', 5))
regions.append(col.subset_for_region('A35-A59').remember('mio_inhabitants', 5))
regions.append(col.subset_for_region('A60-A79').remember('mio_inhabitants', 5))
regions.append(col.subset_for_region('A80+').remember('mio_inhabitants', 5))
CUT_OFF_DAYS = 0

# col = covid.load_for_countries('confirmed.csv', 'deaths.csv', ['Germany', 'Italy', 'Sweden', 'US', 'United Kingdom', 'Denmark', 'Norway'])
# regions.append(col.subset_for_region('Germany').remember('mio_inhabitants', 80))
# regions.append(col.subset_for_region('Italy').remember('mio_inhabitants', 60))
# regions.append(col.subset_for_region('Sweden').remember('mio_inhabitants', 10))
# regions.append(col.subset_for_region('US').remember('mio_inhabitants', 328))
# regions.append(col.subset_for_region('United Kingdom').remember('mio_inhabitants',66))
# regions.append(col.subset_for_region('Denmark').remember('mio_inhabitants', 5))
# regions.append(col.subset_for_region('Norway').remember('mio_inhabitants', 5))
# CUT_OFF_DAYS = 0

for region in regions:
    calculate_basics(region)
    run_interpolations(region)

SELECTED_INDEX = 0
INFECTION_TO_STATISTICS_DELAY = 8
INFECTION_TO_DEATH_STATISTICS_DELAY = 20
R_DELAY = 12
LOOKBACK_DAYS = 48
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

axs[1,0].plot(ctr_timespan.dates(), ctr_timespan.values("new_deaths_weekly"), label='Wöchentlich gemittelt')
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

EVENTS = [{
    datetime.date(2020, 3, 2): "U-Hamsterkäufe",
    datetime.date(2020, 3, 8): "Absage Großveranstaltungen",
    datetime.date(2020, 3, 16): "Schulschließungen",
    datetime.date(2020, 3, 22): "0-Kontaktsperren",
    datetime.date(2020, 4, 10): "Ostern",
    datetime.date(2020, 4, 15): "Lockerungsdiskussionen",
    datetime.date(2020, 4, 27): "Geschäftsöffnungen / Masken",
    datetime.date(2020, 5, 3): "U-Schulöffnungen",
    datetime.date(2020, 5, 6): "Lockerungen Kontaktbeschränkung",
    datetime.date(2020, 5, 15): "U-Gaststättenöffnungen"
    },
    {
        datetime.date(2020, 2, 23): "Absage Karneval",
        datetime.date(2020, 3, 2): "Regionale Lockdowns",
        datetime.date(2020, 3, 12): "Nationaler Lockdown",
        datetime.date(2020, 5, 3): "Fase 2"
        },
    {
        datetime.date(2020, 3, 11): "1. Toter, Keine Vers >500",
        datetime.date(2020, 3, 27): "U-Keine Vers >50",
        datetime.date(2020, 4, 1): "Altenheimbesuche verboten",
        },
    {
        datetime.date(2020, 3, 11): "Schengen Travel ban",
        datetime.date(2020, 3, 16): "15 days to slow the spread",
        datetime.date(2020, 3, 21): "U-Lockdown in many states",
        datetime.date(2020, 4, 15): "Trump: Past the peak",

        },
    {
        datetime.date(2020, 2, 3): "Johnson: Corona-Panic",
        datetime.date(2020, 3, 13): "Herd immunity, isolate elderly",
        datetime.date(2020, 3, 23): "Lockdown",
        datetime.date(2020, 4, 6): "Johnson in ICU"
        },
    {
        datetime.date(2020, 3, 13): "Lockdown",
        datetime.date(2020, 4, 15): "Schulöffnungen"
        },
    {
        datetime.date(2020, 3, 12): "Lockdown",
        datetime.date(2020, 4, 20): "Schulöffnungen"
        }]

infections_realtime = transform_to_realtime(ctr_timespan, INFECTION_TO_STATISTICS_DELAY)
axs[2,0].plot(infections_realtime.dates(), infections_realtime.values("new_infection"), color='lightblue', linestyle='dotted', label='Echtzeit-Infektionen')
axs[2,0].plot(infections_realtime.dates(), infections_realtime.values("new_infections_weekly"), label='Echtzeit-Infektionen (wöchentlich)', color='darkblue')
axs[2,0].plot(infections_realtime.dates(), infections_realtime.values("new_deaths"), label='Echtzeit-Tote', color='orange', linestyle='dotted')
axs[2,0].plot(infections_realtime.dates(), infections_realtime.values("new_deaths_weekly"), label='Echtzeit-Tote (wöchentlich)', color='orange')
axs[2,0].legend()
axs[2,0].set_title("Echtzeit-Neuinfektionen ({})".format(infections_realtime.get("region")))
add_events(EVENTS[SELECTED_INDEX], infections_realtime, "new_infections_weekly", axs[2,0])

r_realtime = transform_to_realtime(ctr_timespan, R_DELAY)
r_deaths_realtime = transform_to_realtime(ctr_timespan, INFECTION_TO_DEATH_STATISTICS_DELAY).subset(lambda c: c.date >= r_realtime.datapoints[0].date)
axs[2,1].plot(r_realtime.dates(), r_realtime.values("r"), color='lightblue', linestyle='dotted', label='Echtzeit-R')
axs[2,1].plot(r_realtime.dates(), r_realtime.values("r_weekly"), label='Echtzeit-R (wöchentlich)', color='darkblue')
axs[2,1].plot(r_deaths_realtime.dates(), r_deaths_realtime.values("r_deaths"), label='Echtzeit-R (aus Toten)', color='orange', linestyle='dotted')
axs[2,1].plot(r_deaths_realtime.dates(), r_deaths_realtime.values("r_deaths_weekly"), label='Echtzeit-R (aus Toten, wöchtl.)', color='orange')
axs[2,1].plot(r_realtime.dates(), [1] * len(r_realtime.dates()), color='red', linestyle='dashed', linewidth=0.5, label='R=1')
axs[2,1].legend()
axs[2,1].set_title("Echtzeit-R ({})".format(infections_realtime.get("region")))

add_events(EVENTS[SELECTED_INDEX], r_realtime, "r_weekly", axs[2,1])
        
plt.show()

