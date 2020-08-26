import pandas as pd
from basic_calculations import calculate_basics, transform_to_realtime, process_region_collection, reduce_weekly
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def calculate_daily_new_infections_per_100k(region_collection):
    def calculate(region_collection, date, item):
        return item.find_calculated("new_infection") / ( region_collection.get("inhabitants") / 100000 )

    return process_region_collection(region_collection, calculate, 'new_infections_per_100k')



eu = pd.read_csv("european-countries.csv")
country_names = eu["Country"].to_list()
inhabitants = eu["Inhabitants"].to_list()

print("IMPORT...")
col = covid.load_for_countries("confirmed.csv", "deaths.csv", country_names)

print("CALCULATION...")
countries = []
for i, country_name in enumerate(country_names):
    print(country_name)
    num_inhabitants = inhabitants[i]
    region = col.subset_for_region(country_name)
    region.remember("name", country_name)
    region.remember('inhabitants', num_inhabitants)
    calculate_basics(region)
    calculate_daily_new_infections_per_100k(region)
    reduce_weekly(region, 'new_infections_per_100k', 'daily_new_infections_per_100k_weekly')

    countries.append(region)

cns = []
p100k1s = []
p100k2s = []
fs = []
for country in countries:
    today = datetime.date.today()
    i1 = country.item_with_date(today - datetime.timedelta(days=7))
    i2 = country.item_with_date(today - datetime.timedelta(days=14))
    if ( i1 != None ) and ( i2 != None ):
        p100k1 = i1.find_calculated("daily_new_infections_per_100k_weekly")
        p100k2 = i2.find_calculated("daily_new_infections_per_100k_weekly")
        if p100k2 > 0:
            f = p100k1 / p100k2
        else:
            f = 0
        cns.append(country.get("name"))
        p100k1s.append(p100k1)
        p100k2s.append(p100k2)
        fs.append(f)
        # print(country.get("name") + ": letzte Woche " + str(p100k1) + ", vorletzte Woche: " + str(p100k2) + ", f=" + str(f))

df = pd.DataFrame({"name": cns, "Letzte Woche": p100k1s, "Vorletzte Woche": p100k2s, "Faktor": fs})
print(df.sort_values(by=['Letzte Woche'], ascending=False))
# print(df)


