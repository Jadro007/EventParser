import io
import sys
import os
import requests
import csv

from bs4 import BeautifulSoup

from config import config

from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def write_response(html, filedir, filename):
    filename += ".html"
    filepath = os.path.join(filedir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)


url = sys.argv[1]
filename = "".join(x for x in url if x.isalnum()).strip("httpswww").strip("httpwww")
r = requests.get(url, allow_redirects=True)
html = r.content
soup = BeautifulSoup(html, 'html.parser')

test_dir = "./data/test2"
write_response(str(soup), test_dir, filename)

events = EventParser.parse(html)
data = []
for event in events:
    price = "none"
    if event.priceRange is not None:
        price = event.priceRange.priceFrom.text + " - " + event.priceRange.priceTo.text
    found_date = event.date
    found_date_value = '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(found_date.dateFrom.datetime.month) + ". " + str(found_date.dateFrom.datetime.year)

    if found_date.dateFrom.datetime != found_date.dateTo.datetime:
        found_date_value = (
                '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(found_date.dateFrom.datetime.month) + ". - " +
                '{:02d}'.format(found_date.dateTo.datetime.day) + ". " + '{:02d}'.format(found_date.dateTo.datetime.month) + ". " + str(found_date.dateTo.datetime.year)
        )

    print("Name: " + event.title.value + "("+event.title.alternative_value+"), ",
             "date: " + found_date_value + ", place: " + event.place.city,
          "price: " + price, "score:" + str(event.score))
    data.append([
        event.title.value + "(" + event.title.alternative_value + ")",
        found_date_value,
        "",
        event.place.city
    ])


with open(test_dir + "/" + filename + ".txt", "w", newline='', encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    for line in data:
        writer.writerow(line)

f = open(test_dir + "/" + filename + "_url.txt", "w")
f.write(url)
f.close()