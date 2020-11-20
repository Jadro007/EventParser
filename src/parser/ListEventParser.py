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
        groups = {}
        for date in dates:
            group_repr = repr(date.group)
            if date.group is not None and group_repr not in groups:
                groups[group_repr] = date.group

        for key, group in groups.items():
            children = group.container.findChildren()
            for child in children:
                event = SingleEventParser.parse(child)
                if event is not None:
                    events.append(event)

        for event in events:
            event.container.extract()  # event was successfully found, we can now safely remove it

        return events





