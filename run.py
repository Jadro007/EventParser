import io
import sys
import requests
import time

from config import config
from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

start_time = time.time()

html = None
# if __name__ == '__main__':
# url = sys.argv[1]



url = "https://www.zemezivitelka.cz/"
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
    events = EventParser.parse(html)

print("FOUND EVENTS")

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

    print("Name: " + event.title.value + "("+event.title.alternative_value+"), ",
             "date: " + found_date_value + ", place: " + event.place.city,
          "price: " + price, "score:" + str(event.score))

print("--- %s seconds ---" % (time.time() - start_time))