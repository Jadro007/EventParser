import io
import sys

from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

path = "./data/test/23 Zumba s jógou - wellness víkend v Janských lázních - ZUMBA FITNESS.html"
html = open(path, 'r', errors='ignore', encoding="utf-8").read()

events = EventParser.parse(html)

print("HELLOOOOO")

for event in events:
    price = "none"
    if event.priceRange is not None:
        price = event.priceRange.priceFrom.text + " - " + event.priceRange.priceTo.text

    print("Name: " + event.title.value + ", date: " + event.date.realValue + ", place: " + event.place.city, "price: " + price)
