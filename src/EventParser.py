import sys
import re

from bs4 import BeautifulSoup

from src.dto.Event import Event
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.ListEventParser import ListEventParser
from src.parser.SingleEventParser import SingleEventParser
from src.postprocessing.DuplicateEventsPostprocessor import DuplicateEventPostprocessor
from src.postprocessing.YearPostprocessor import YearPostprocessor
from src.preprocessing.DatePreprocessor import DatePreprocessor
from src.preprocessing.RemovalPreprocessor import RemovalPreprocessor
from src.scoring.EventScoring import EventScoring
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from config import shared

class EventParser:

    @staticmethod
    def parse_url(url) -> [Event]:
        options = Options()
        options.headless = True
        shared.driver = Chrome(options=options, executable_path='lib/chromedriver.exe')
        shared.driver.get(url)

        html = shared.driver.page_source
        return EventParser.parse(html)

    @staticmethod
    def parse(html) -> [Event]:
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

        # try to parse Events separated in groups
        groups = {}
        for date in dates:
            if date.group is not None:
                groups[repr(date.group)] = date.group

        events = []
        for group in groups:
            events.extend(ListEventParser.parse(soup, groups[group].dates))

        dates = DateFinder.find(soup)
        single_event_without_place_counter = 0
        single_event_counter = 0
        # todo: refactor this
        # go through all single events
        # If all of them do not have place, allow usage of external place
        for date in dates:
            if date.group is None:
                single_event_counter += 1
                single_event = SingleEventParser.parse(soup, date)
                if single_event == SingleEventParser.NO_PLACE_REASON:
                    single_event_without_place_counter += 1
                    continue
                if single_event is not None:
                    events.append(single_event)
        if single_event_without_place_counter == single_event_counter:
            for date in dates:
                if date.group is None:
                    single_event = SingleEventParser.parse(soup, date, True)
                    if single_event == SingleEventParser.NO_PLACE_REASON:
                        continue
                    if single_event is not None:
                        events.append(single_event)

        YearPostprocessor.fix_year(events)

        events = DuplicateEventPostprocessor.filter_duplicates(events)

        EventScoring.score_events(events)

        if shared.driver is not None:
            shared.driver.close()
        return events


# if __name__ == '__main__':
#     # path = sys.argv[1]
#     path = "./test/26 Trabantem napříč kontinenty – vstupenky _ smsticket.txt"
#     html = open(path, 'r', errors='ignore', encoding="utf-8").read()
#     EventParser.parse(html)
