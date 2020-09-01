from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime


def plot_share(ax, timespan, names, datasets):
    daily_sums = [np.sum([dataset[i] for dataset in datasets]) for i in range(0, len(timespan))]
    daily_shares = [[dataset[i] / daily_sums[i] for i in range(0, len(timespan))] for dataset in datasets]
    plot_stacked(ax, timespan, names, daily_shares)

def plot_stacked(ax, timespan, names, daily_shares):
    sums = None
    for i, daily_share in enumerate(daily_shares):
        if i==0:
            ax.bar(timespan, daily_share, label=names[i], color=COLORS[i])
            sums = np.array(daily_share)
        else:
            ax.bar(timespan, daily_share, label=names[i], bottom=sums, color=COLORS[i])
            sums = sums + np.array(daily_share)


DATE_START = datetime.date(2020, 3, 1)
DATE_START_DEATHS = datetime.date(2020, 3, 14)
DATE_END = datetime.date.today() - datetime.timedelta(days=2)

AGE_GROUPS = ['A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 'A80+']
COLORS = ['lightgreen', 'limegreen', 'forestgreen', 'lightskyblue', 'lightcoral', 'red']
col = covid.load_for_countries('rki-confirmed.csv', 'rki-deaths.csv', AGE_GROUPS)
age_groups = []
age_groups.append(col.subset_for_region('A00-A04'))
age_groups.append(col.subset_for_region('A05-A14'))
age_groups.append(col.subset_for_region('A15-A34'))
age_groups.append(col.subset_for_region('A35-A59'))
age_groups.append(col.subset_for_region('A60-A79'))
age_groups.append(col.subset_for_region('A80+'))

for age_group in age_groups:
    calculate_basics(age_group)
    run_interpolations(age_group)


timespan = age_groups[0].subset_for_timespan(DATE_START, DATE_END).dates()
timespan_deaths = age_groups[0].subset_for_timespan(DATE_START_DEATHS, DATE_END).dates()
names = [age_group.datapoints[0].region for age_group in age_groups]

fig, axs = plt.subplots(3, 2)

ax = axs[0,0]
datasets_infection_wkly = [np.array(age_group.subset_for_timespan(DATE_START, DATE_END).values("new_infections_weekly_sum")) for age_group in age_groups]
plot_stacked(ax, timespan, names, datasets_infection_wkly)
ax.set_title("Absoluter Anteil der Altersgruppen an den Neuinfektionen")
ax.legend()

ax = axs[0,1]
datasets_infection_wkly = [np.array(age_group.subset_for_timespan(DATE_START, DATE_END).values("new_deaths_weekly")) for age_group in age_groups]
plot_stacked(ax, timespan, names, datasets_infection_wkly)
ax.set_title("Absoluter Anteil der Altersgruppen an den Toten")
ax.legend()

ax = axs[1,0]
datasets_infection = [np.array(age_group.subset_for_timespan(DATE_START, DATE_END).values("new_infection")) for age_group in age_groups]
plot_share(ax, timespan, names, datasets_infection)
ax.set_title("Anteil der Altersgruppen an den Neuinfektionen")
ax.legend()

ax = axs[1,1]
datasets_deaths = [np.array(age_group.subset_for_timespan(DATE_START_DEATHS, DATE_END).values("new_deaths_weekly")) for age_group in age_groups]
plot_share(ax, timespan_deaths, names, datasets_deaths)
ax.set_title("Anteil der Altersgruppen an den Toten")
ax.legend()

ax = axs[2,0]
sums_infections = [np.sum(dataset) for dataset in datasets_infection]
deaths_daily = [np.array(age_group.subset_for_timespan(DATE_START_DEATHS, DATE_END).values("new_deaths")) for age_group in age_groups]
sums_deaths = [np.sum(dataset) for dataset in deaths_daily]
rates = [(sums_deaths[i] / sums_infections[i] * 100)  for i, _ in enumerate(age_groups)]
ax.bar(names, rates)
ax.set_title("Fallsterblichkeit nach Alter")
ax.set_ylabel("in % der Fälle")

print(rates)
plt.show()
