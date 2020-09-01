from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

CUT_OFF_DAYS = 3
LOOKBACK_DAYS = 90

AGE_GROUPS = ['A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 'A80+']
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

fig, axs = plt.subplots(3, 2)

today = datetime.date.today() - datetime.timedelta(days=CUT_OFF_DAYS)
daysago = today - datetime.timedelta(days=LOOKBACK_DAYS)

for i, age_group in enumerate(age_groups):
    timespan_data = age_group.subset_for_timespan(daysago, today)

    row = int(i / 2)
    col = i % 2
    name = age_group.datapoints[0].region
    axs[row, col].set_ylabel('Neuinfektionen')
    axs[row, col].plot(timespan_data.dates(), timespan_data.values("new_infections_weekly_sum"), label="Wöchentliche Summe", color='blue')
    axs[row, col].plot(timespan_data.dates(), timespan_data.values("new_infection"), color='lightgray', linestyle='dotted', label='Täglich')

    # axr = axs[row, col].twinx()
    # axr.set_ylabel('R (wöchentlich)')
    # axr.plot(timespan_data.dates(), timespan_data.values("r_weekly"), label="R (wöchentlich)", color='orange')
    # axr.plot(timespan_data.dates(), [1] * len(timespan_data.dates()), color='red', label='R=1', linestyle='dashed', linewidth=0.5)

    axs[row,col].legend()
    axs[row, col].set_title(name)



plt.show()
