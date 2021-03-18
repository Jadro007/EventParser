import re

from typing import Optional

from bs4 import BeautifulSoup

from src import utils
from src.dto.Description import Description
from src.dto.Event import Event
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.finder.CategoryFinder import CategoryFinder
from src.utils.Utils import Utils


class DescriptionFinder:

    @staticmethod
    def add_description(events) -> [Event]:

        for event in events:
            common_container = event.small_container
            if common_container is None:
                common_container = event.container

            longest_text_elem = DescriptionFinder.find_description_element(common_container)
            if longest_text_elem is None or (len(longest_text_elem.text) < 300 and (event.category == CategoryFinder.SINGLE_EVENT or event.category == CategoryFinder.SINGLE_EVENT_WITH_TIMELINE)):
                longest_text_elem = DescriptionFinder.find_description_element(common_container.parent)

            if longest_text_elem is None:
                continue

            event.description = Description(Utils.clean(longest_text_elem.text), longest_text_elem)

        return events

    @staticmethod
    def find_description_element(common_container):
        if common_container is None:
            return None
        longest_text = 0
        longest_text_elem = None
        for elem in common_container.find_all():  # text=True
            elem = Utils.getTag(elem)
            text = elem.text
            text_len = len(text)
            if longest_text_elem is None or text_len > longest_text:
                longest_text_elem = elem
                longest_text = text_len
        if longest_text < 300:
            longest_text_elem = common_container
        return longest_text_elem
