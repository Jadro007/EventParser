import sys
import re

from bs4 import BeautifulSoup

from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.ListEventParser import ListEventParser
from src.parser.SingleEventParser import SingleEventParser
from src.preprocessing.DatePreprocessor import DatePreprocessor
from src.preprocessing.RemovalPreprocessor import RemovalPreprocessor


class EventParser:

    @staticmethod
    def parse(html):
        print("WELCOME")
        soup = BeautifulSoup(html, 'html.parser')

        print("CLEANING THE HTML DOCUMENT")
        print("REMOVING COMMENTS")
        soup = RemovalPreprocessor.remove_comments(soup)
        print("REMOVING SCRIPT AND STYLE TAG")
        soup = RemovalPreprocessor.remove_script_and_style_tag(soup)
        print("FIXING BROKEN DATES")
        soup = DatePreprocessor.fix_dates(soup)

        print("STARTING TO FIND EVENTS")

        dates = DateFinder.find(soup)

        print("FOUND", len(dates), "DATES")

        events = ListEventParser.parse(soup, dates)

        dates = DateFinder.find(soup)
        for date in dates:
            if date.group is None:
                events.append(SingleEventParser.parse(soup, date))

        return events


# if __name__ == '__main__':
#     # path = sys.argv[1]
#     path = "./test/26 Trabantem napříč kontinenty – vstupenky _ smsticket.txt"
#     html = open(path, 'r', errors='ignore', encoding="utf-8").read()
#     EventParser.parse(html)
