import re

from typing import Optional

from bs4 import BeautifulSoup

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Time import Time
from src.utils.Utils import Utils




class CategoryFinder:
    LIST_EVENT_WITH_TIMELINE = "list_event_with_timeline"
    SINGLE_EVENT_WITH_TIMELINE = "single_event_with_timeline"
    SINGLE_EVENT = "single_event"
    LIST_EVENT = "list_event"

    @staticmethod
    def add_category(events):

        for event in events:
            category = CategoryFinder.LIST_EVENT

            if event.date.dateFrom.group is None:
                category = CategoryFinder.SINGLE_EVENT

                if len(event.times) > 2:
                    category = CategoryFinder.SINGLE_EVENT_WITH_TIMELINE
            elif len(event.times) > 2:
                category = CategoryFinder.LIST_EVENT_WITH_TIMELINE

            event.category = category

