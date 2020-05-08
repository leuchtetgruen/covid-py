import covid
import basic_calculations
import numpy as np

def interpolate(region_collection, source_key, target_key, ifr):
    def calculate(region_collection, date, item):
        return item.find_calculated(source_key) * ( item.find_calculated("cfr") / ifr )

    return basic_calculations.process_region_collection(region_collection, calculate, target_key)


def interpolate_cases(region_collection, ifr):
    return interpolate(region_collection, 'confirmed', 'interpolated_cases', ifr)


def interpolate_new_infections(region_collection, ifr):
    return interpolate(region_collection, 'new_infection', 'interpolated_new_infection', ifr)

def interpolate_active_cases(region_collection, ifr):
    return interpolate(region_collection, 'active_cases', 'interpolated_active_cases', ifr)




def run_interpolations(region_collection, ifr=0.005):
    interpolate_cases(region_collection, ifr)
    interpolate_new_infections(region_collection, ifr)
    interpolate_active_cases(region_collection, ifr)

    return region_collection
