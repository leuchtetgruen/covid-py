import datetime
import pandas as pd
import numpy as np
import pdb
from rki import RKIDataPoint, load_rki_csv
from rki_tools import for_region, for_age_bracket, for_timespan, for_week, AGE_BRACKETS, REGIONS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


data = load_rki_csv("./rki.csv")
print("RKI datapoints have been loaded into the data variable")
print("Use the for_... functions. pass the list as the first parameter and the conditions as the 2nd (and 3rd) parameter")
print("for_region, for_age_bracket, for_timespan, for_week")
print("Use the variables AGE_BRACKETS and REGIONS to see and use available regions and age brackets.")
pdb.set_trace()
