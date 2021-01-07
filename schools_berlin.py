from basic_calculations import calculate_basics, transform_to_realtime
from interpolation import run_interpolations
import prognosis
import covid
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys

LK_ID = '11000'
col = covid.load_for_countries('rki-confirmed.csv', 'rki-deaths.csv', [LK_ID])
regions.append(col.subset_for_region(LK_ID).remember('mio_inhabitants', 5))
