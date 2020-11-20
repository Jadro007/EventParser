import io
import sys

from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

path = "./data/test/26 Trabantem napříč kontinenty – vstupenky _ smsticket.html"
html = open(path, 'r', errors='ignore', encoding="utf-8").read()

events = EventParser.parse(html)

print("HELLOOOOO")

for event in events:
    print("Name: " + event.title + ", date: " + event.date.realValue + ", place: " + event.place.city)
