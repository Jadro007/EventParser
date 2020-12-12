import sys
import re

from bs4 import BeautifulSoup

from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.ListEventParser import ListEventParser
from src.parser.SingleEventParser import SingleEventParser
from src.postprocessing.DuplicateEventsPostprocessor import DuplicateEventPostprocessor
from src.postprocessing.YearPostprocessor import YearPostprocessor
from src.preprocessing.DatePreprocessor import DatePreprocessor
from src.preprocessing.RemovalPreprocessor import RemovalPreprocessor


class EventParser:

    @staticmethod
    def parse(html):
        print("WELCOME")
        soup = BeautifulSoup(html, 'html.parser')

        print("CLEANING THE HTML DOCUMENT")

        print("REMOVING COMMENTS, REMOVING SCRIPT AND STYLE TAG")
        soup = RemovalPreprocessor.cleanup(soup)

        print("FIXING BROKEN DATES")
        soup = DatePreprocessor.fix_dates(soup)
        print("PREPARING DATE RANGES")
        soup = DatePreprocessor.prepare_date_ranges(soup)

        print("UNWRAPPING ELEMENTS")
        soup = RemovalPreprocessor.unwrap(soup)

        # reloading the tree helps for some reason
        soup = BeautifulSoup(str(soup), 'html.parser')

        # print("WRITING OUTPUT FOR DEBUGGING TO test.html")
        # with open("test.html", 'w', errors='ignore', encoding="utf-8") as file:
        #     file.write(str(soup))
        # exit(1)

        print("STARTING TO FIND EVENTS")
        dates = DateFinder.find(soup)
        print("FOUND", len(dates), "DATES")

        events = ListEventParser.parse(soup, dates)

        dates = DateFinder.find(soup)
        for date in dates:
            if date.group is None:
                single_event = SingleEventParser.parse(soup, date)
                if single_event is not None:
                    events.append(single_event)


        YearPostprocessor.fix_year(events)

        events = DuplicateEventPostprocessor.filter_duplicates(events)

        return events


# if __name__ == '__main__':
#     # path = sys.argv[1]
#     path = "./test/26 Trabantem napříč kontinenty – vstupenky _ smsticket.txt"
#     html = open(path, 'r', errors='ignore', encoding="utf-8").read()
#     EventParser.parse(html)
