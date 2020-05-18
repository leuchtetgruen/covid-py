import datetime
import pandas as pd

class RKIDataPoint:
    def __init__(self, date_str, age_bracket, count, death_count, region_id):
        self.date = self.to_date(date_str)
        self.age_bracket = age_bracket
        self.count = count
        self.death_count = death_count
        self.region_id = region_id

    def to_date(self, date_str):
        date_component = date_str.split(" ")[0]
        date_components = [int(x) for x in date_component.split("/")]
        return datetime.date(date_components[0], date_components[1], date_components[2])


def rki_row_to_rki_datapoint(row):
    return RKIDataPoint(row['Meldedatum'], row['Altersgruppe'], row['AnzahlFall'], row['AnzahlTodesfall'], row['IdLandkreis'])

def load_rki_csv(filename):
    print("Reading data...")
    df = pd.read_csv("./rki.csv")
    print("Converting to Datapoints")
    return [rki_row_to_rki_datapoint(x) for i,x in df.iterrows()]
