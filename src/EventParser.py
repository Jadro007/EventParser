import sys
import re

from bs4 import BeautifulSoup

from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.ListEventParser import ListEventParser
from src.parser.SingleEventParser import SingleEventParser


class EventParser:

    @staticmethod
    def parse(html):
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        events = ListEventParser.parse(soup, dates)

        dates = DateFinder.find(soup)
        for date in dates:
            if date.group is None:
                events.append(SingleEventParser.parse(soup))

        return events


# if __name__ == '__main__':
#     # path = sys.argv[1]
#     path = "./test/26 Trabantem napříč kontinenty – vstupenky _ smsticket.txt"
#     html = open(path, 'r', errors='ignore', encoding="utf-8").read()
#     EventParser.parse(html)
