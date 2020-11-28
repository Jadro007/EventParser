from bs4 import BeautifulSoup
import re

from src.dto.Date import Date
from src.dto.Event import Event
from src.dto.Place import Place
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.SingleEventParser import SingleEventParser
from src.utils.Utils import Utils


class ListEventParser:

    @staticmethod
    def parse(soup, dates: [Date]):

        events = []
        # THIS WAS NOT WORKING PROPERLY, REPLACED WITH NEW CODE
        # groups = {}
        # for date in dates:
        #     group_repr = repr(date.group)
        #     if date.group is not None and group_repr not in groups:
        #         groups[group_repr] = date.group
        #
        # for key, group in groups.items():
        #     children = group.container.findChildren()
        #     for child in children:
        #         event = SingleEventParser.parse(child)
        #         if event is not None:
        #             events.append(event)

        # for each date we will try to find event
        for date in dates:
            # in ListEventParser, we only care about dates that are part of group of dates
            if date.group is None:
                continue

            # Here we will find maximum container, that contains only the one date, but does not contain other dates.
            # This is achieved by having already the event divided into groups, so group.container - 1 length is
            # what we are looking for. So we traverse there from the date to have correct part of the tree.
            previous_parent = None
            parent = date.container
            while repr(parent) != repr(date.group.container):
                previous_parent = parent
                parent = parent.parent

            event = SingleEventParser.parse(previous_parent, date)
            if event is not None:
                events.append(event)

        for event in events:
            event.container.extract()  # event was successfully found, we can now safely remove it

        return events





