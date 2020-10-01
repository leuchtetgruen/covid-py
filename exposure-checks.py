import json
import sys
import pdb
import datetime


def parse_date(datestr):
    trans = [
            ["Januar", "January"],
            ["Februar", "February"],
            ["März", "March"],
            ["Mai", "May"],
            ["Juni", "June"],
            ["Juli", "July"],
            ["Oktober", "October"],
            ["Dezember", "December"],
            ]

    for month in trans:
        datestr = datestr.replace(month[0], month[1])

    return datetime.datetime.strptime(datestr, '%d. %B %Y, %H:%M')


filename = sys.argv[1]
date_sorted = {}
found_count = {}
with open(filename) as json_file:
    data = json.load(json_file)

for item in data:
    date = parse_date(item['timestamp'])
    if date_sorted.get(date) == None:
        date_sorted[date] = []

    date_sorted[date].append(item)


for date in date_sorted:
    print("Checking for {}...".format(date.date()))
    for idx, item in enumerate(date_sorted[date]):
        days_ago = 14 - idx
        target_date = date.date() - datetime.timedelta(days=days_ago)
        counter = 0
        if found_count.get(target_date) != None:
            counter = found_count.get(target_date)

        if item['matchesCount'] > 0:
            print(" Found {} matches {} days ago".format(item['matchesCount'], days_ago))

        counter = counter + item['matchesCount']
        found_count[target_date] = counter

print("")
for date in found_count:
    str_found = "0"
    if (found_count[date] > 0):
        print("Exposures on {} : >0 - found in datasets of {} days".format(date, found_count[date]))
