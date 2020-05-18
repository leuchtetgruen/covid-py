import datetime
import pandas as pd
import numpy as np
import pdb
from rki import RKIDataPoint, load_rki_csv

data = load_rki_csv("./rki.csv")
print("RKI datapoints have been loaded into the data variable")
pdb.set_trace()
