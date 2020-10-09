import datetime
import pandas as pd

def to_date(date_str):
    if ((type(date_str) != str)):
        return None

    date_components = [int(i) for i in date_str.split(".")]
    dt = datetime.date(date_components[2], date_components[1], date_components[0])
    return dt

def rate_for_day(day):
    index = DATES.index(day)
    return VALUES[index]


df = pd.read_csv("positivquote.csv", sep=';')
DATES = [to_date(i) for i in df["Tag"].to_numpy()]
VALUES = [float(str(i).replace(',' , '.').replace('nan','0')) for i in df["Positivenquote"].to_numpy()]
