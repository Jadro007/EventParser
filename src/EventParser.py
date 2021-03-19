import sys
import re

from bs4 import BeautifulSoup

from src.dto.Event import Event
from src.finder.CategoryFinder import CategoryFinder
from src.finder.DescriptionFinder import DescriptionFinder
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.finder.TargetUrlFinder import TargetUrlFinder
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
from config import config
from src.scoring.NerScoring import NerScoring
from src.utils.Utils import Utils


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
    def parse(html, url = "") -> [Event]:
        if config.verbose >= 1:
            print("WELCOME")
        soup = BeautifulSoup(html, 'html.parser')

        if config.verbose >= 1:
            print("CLEANING THE HTML DOCUMENT")

        if config.verbose >= 1:
            print("REMOVING COMMENTS, REMOVING SCRIPT AND STYLE TAG")
        soup = RemovalPreprocessor.cleanup(soup)

        if config.verbose >= 1:
            print("FIXING BROKEN DATES")
        soup = DatePreprocessor.fix_dates(soup)

        if config.verbose >= 1:
            print("PREPARING DATE RANGES")
        soup = DatePreprocessor.prepare_date_ranges(soup)

        if config.verbose >= 1:
            print("UNWRAPPING ELEMENTS")
        soup = RemovalPreprocessor.unwrap(soup)

        # reloading the tree helps for some reason
        soup_str = str(soup)
        soup_str.replace(u'\xa0', " ")
        soup_str.replace('&nbsp;', " ")

        soup_str = DatePreprocessor.fix_today_and_tomorrow(soup_str)

        soup = BeautifulSoup(soup_str, 'html.parser')

        i = 1
        for tag in soup.findAll(True):
            tag.custom_id = i
            i += 1

        # print("WRITING OUTPUT FOR DEBUGGING TO test.html")
        # with open("test.html", 'w', errors='ignore', encoding="utf-8") as file:
        #     file.write(str(soup))
        # exit(1)

        if config.verbose >= 1:
            print("STARTING TO FIND EVENTS")
        dates = DateFinder.find(soup)
        if config.verbose >= 1:
            print("FOUND", len(dates), "DATES")

        # try to parse Events separated in groups
        groups = {}
        for date in dates:
            if date.group is not None:
                groups[Utils.getCustomId(date.group.container)] = date.group

        events = []
        for group in groups:
            events.extend(ListEventParser.parse(soup, groups[group].dates))

        # dates = DateFinder.find(soup)
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

        CategoryFinder.add_category(events)

        DescriptionFinder.add_description(events)

        TargetUrlFinder.add_target_url(events, url)

        for event in events:
            event.source_url = url

        YearPostprocessor.fix_year(events)

        events = DuplicateEventPostprocessor.filter_duplicates(events)

        EventScoring.score_events(events)
        NerScoring.score_events(events)

        if shared.driver is not None:
            shared.driver.close()
        return events


# if __name__ == '__main__':
#     # path = sys.argv[1]
#     path = "./test/26 Trabantem napříč kontinenty – vstupenky _ smsticket.txt"
#     html = open(path, 'r', errors='ignore', encoding="utf-8").read()
#     EventParser.parse(html)
