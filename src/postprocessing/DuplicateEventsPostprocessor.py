import re

from typing import Optional

from bs4 import BeautifulSoup
import datetime
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.utils.Utils import Utils


class DuplicateEventPostprocessor:
    year_regex_compiled = re.compile("(\d{4})")


    @staticmethod
    def filter_duplicates(events):
        new_events = {}

        for event in events:
            key = (
                    event.title.value +
                    event.place.city +
                    repr(event.date.dateFrom.datetime) + repr(event.date.dateTo.datetime)
            )

            new_events[key] = event

        return list(new_events.values())
