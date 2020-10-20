from basic_calculations import calculate_basics, transform_to_realtime, process_region_collection
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from testrates import rate_for_day



def plot_stacked(ax, timespan, names, daily_shares):
    sums = None
    for i, daily_share in enumerate(daily_shares):
        if i==0:
            ax.bar(timespan, daily_share, label=names[i], color=COLORS[i])
            sums = np.array(daily_share)
        else:
            ax.bar(timespan, daily_share, label=names[i], bottom=sums, color=COLORS[i])
            sums = sums + np.array(daily_share)

def predict_case_fatality_rate(region_collection, cfr):
    def calculate(region_collection, date, item):
            return item.find_calculated("new_infections_weekly") * cfr
    return process_region_collection(region_collection, calculate, 'predicted_cfr')

def predict_hospitalization(region_collection, hospitalization_rate):
    def calculate(region_collection, date, item):
        return item.find_calculated("new_infections_weekly") * hospitalization_rate

    return process_region_collection(region_collection, calculate, 'predicted_hospitalization')

def test_positive_adjusted_value(region_collection):
    def calculate(region_collection, date, item):
        return item.find_calculated("new_infections_weekly") * (rate_for_day(date) / 2) # 2 is a target for tpr

    return process_region_collection(region_collection, calculate, 'new_infections_adjusted')


DATE_START = datetime.date(2020, 3, 1)
DATE_END = datetime.date.today() - datetime.timedelta(days=5)

HOSPITALISIERUNG = 0.14
AGE_GROUPS = ['A60-A79', 'A80+', '7654321']
CASE_FATALITY_RATES = [0.067, 0.247]
COLORS = ['lightcoral', 'red']
col = covid.load_for_countries('rki-confirmed.csv', 'rki-deaths.csv', AGE_GROUPS)
age_groups = []
age_groups.append(col.subset_for_region('A60-A79'))
age_groups.append(col.subset_for_region('A80+'))

all_ages = col.subset_for_region('7654321')

all_ages = col.subset_for_region('7654321')

for i, age_group in enumerate(age_groups):
    calculate_basics(age_group)
    run_interpolations(age_group)
    predict_case_fatality_rate(age_group, CASE_FATALITY_RATES[i])

calculate_basics(all_ages)
run_interpolations(all_ages)
predict_hospitalization(all_ages, HOSPITALISIERUNG)
test_positive_adjusted_value(all_ages)

timespan = age_groups[0].subset_for_timespan(DATE_START, DATE_END).dates()
names = [age_group.datapoints[0].region for age_group in age_groups]

fig, axs = plt.subplots(2, 2)

ax = axs[0,0]
datasets_infection_wkly = [np.array(age_group.subset_for_timespan(DATE_START, DATE_END).values("new_infections_weekly")) for age_group in age_groups]
plot_stacked(ax, timespan, names, datasets_infection_wkly)
ax.set_title("Anzahl der Infizierten in den Altersgruppen >60")
ax.legend()

ax = axs[0,1]
cfr_stacks = [np.array(age_group.subset_for_timespan(DATE_START, DATE_END).values("predicted_cfr")) for age_group in age_groups]
plot_stacked(ax, timespan, names, cfr_stacks)
ax.set_title("Vorhersage resultierende Tote (nachlaufend)")
ax.legend()

ax = axs[1,0]
all_ages_with_timespan = all_ages.subset_for_timespan(DATE_START, DATE_END)
ax.plot(all_ages_with_timespan.dates(), all_ages_with_timespan.values("new_infections_adjusted"))
ax.set_title("Testpositivkorrigierte Neuinfektionen")
ax.set_yticklabels([])
ax.legend()

ax = axs[1,1]
all_ages_with_timespan = all_ages.subset_for_timespan(DATE_START, DATE_END)
ax.plot(all_ages_with_timespan.dates(), all_ages_with_timespan.values("predicted_hospitalization"), color='gray')
ax.set_title("Vorhergesage Neu-Hospitalisierung (nachlaufend) ohne Altersabhängigkeit*")
ax.legend()



plt.show()
