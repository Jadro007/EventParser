#!/usr/bin/env python3


import io
import sys
import requests
import time
import getopt

from src.serializer.EventsJSONSerializer import EventsJSONSerializer

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, dir_path)
sys.path.insert(0, dir_path + "/lib/")


from config import config
from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

start_time = time.time()

html = None
# if __name__ == '__main__':
help_text = 'run.py url [--allow-poi, [--verbose int, [--help]]]'
if len(sys.argv) == 1:
    print(help_text)
    exit(2)

url = sys.argv[1]
argv = sys.argv[2:]

try:
    opts, args = getopt.getopt(argv, "hpv:", ["allow-poi", "verbose int"])
except getopt.GetoptError:
    print(help_text)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', "--help"):
        print(help_text)
        sys.exit()
    elif opt in ("-p", "--allow-poi"):
        config.allow_poi = True
    elif opt in ("-v", "--verbose"):
        config.verbose = int(arg)

# url = None
path = None
# path = "./data/test2/informujiczakcezitrahudba.html"
if path is None:
    r = requests.get(url, allow_redirects=True)
    html = r.content
else:
    html = open(path, 'r', errors='ignore', encoding="utf-8").read()


if html is None:
    events = EventParser.parse_url(url)
else:
    events = EventParser.parse(html, url)

# print("FOUND EVENTS")

# for event in events:
#     price = "none"
#     if event.priceRange is not None:
#         price = event.priceRange.priceFrom.text + " - " + event.priceRange.priceTo.text
#     found_date = event.date
#     found_date_value = '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(found_date.dateFrom.datetime.month) + ". " + str(found_date.dateFrom.datetime.year)
#
#     if found_date.dateFrom.datetime != found_date.dateTo.datetime:
#         found_date_value = (
#                 '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(found_date.dateFrom.datetime.month) + " - " +
#                 '{:02d}'.format(found_date.dateTo.datetime.day) + ". " + '{:02d}'.format(found_date.dateTo.datetime.month) + ". " + str(found_date.dateTo.datetime.year)
#         )
#
#     print("Name: " + event.title.value + "("+event.title.alternative_value+"), ",
#              "date: " + found_date_value + ", place: " + event.place.city,
#           "price: " + price, "score:" + str(event.score))

print(EventsJSONSerializer.serialize(events))

if config.verbose > 2:
    print("--- %s seconds ---" % (time.time() - start_time))