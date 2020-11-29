import io
import sys

from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

path = "./data/test/3 Kudy z nudy - Vánoční výstava v Galerii Mariette ve Vizovicích.html"
html = open(path, 'r', errors='ignore', encoding="utf-8").read()

events = EventParser.parse(html)

print("HELLOOOOO")

for event in events:
    price = "none"
    if event.priceRange is not None:
        price = event.priceRange.priceFrom.text + " - " + event.priceRange.priceTo.text
    found_date = event.date
    found_date_value = '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(found_date.dateFrom.datetime.month) + ". " + str(found_date.dateFrom.datetime.year)

    if found_date.dateFrom.datetime != found_date.dateTo.datetime:
        found_date_value = (
                '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(found_date.dateFrom.datetime.month) + " - " +
                '{:02d}'.format(found_date.dateTo.datetime.day) + ". " + '{:02d}'.format(found_date.dateTo.datetime.month) + ". " + str(found_date.dateTo.datetime.year)
        )

    print("Name: " + event.title.value + ", date: " + found_date_value + ", place: " + event.place.city, "price: " + price)
