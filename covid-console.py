import datetime
import pandas as pd
import numpy as np
import pdb
import covid
import basic_calculations
import interpolation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

print("Loading data...")
PREFIX = "rki-"
subsets = ['A00-A04', 'A05-A14', 'A15-A34', 'A35-A59', 'A60-A79', 'A80+']
data = covid.load_for_countries(PREFIX + 'confirmed.csv', PREFIX + 'deaths.csv', subsets, False)

list_subsets = [data.subset_for_region(x) for x in subsets]

for item in list_subsets:
    basic_calculations.calculate_basics(item)
    interpolation.run_interpolations(item)

pdb.set_trace()
