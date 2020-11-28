from bs4 import BeautifulSoup
import re

from config.config import verbose
from src.dto.Event import Event
from src.finder.PriceFinder import PriceFinder
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.finder.TitleFinder import TitleFinder
from src.utils.Utils import Utils


class SingleEventParser:

    @staticmethod
    def parse(soup):

        # todo: support multiple dates events (including date range)
        try:
            date = DateFinder.find(soup)[0]
        except IndexError:
            if verbose > 2:
                print("Found event without date, skipping")
            return None

        try:
            place = PlaceFinder.find(soup)[0]
        except IndexError:
            if verbose > 2:
                print("Found event without place with date: " + date.realValue + ", skipping")
            return None

        price_range = PriceFinder.find(soup)

        # we want to be able to find the most relevant title for event, so we will start with container that contains
        # both date and place, so there is quite chance there will be also the title
        container = Utils.lowest_common_ancestor(date.container, place.container)
        title = TitleFinder.find(container.parent)
        if title is None:
            if verbose > 2:
                print("Found event without title (date: " + date.realValue + ", place: " + place.city + "), skipping")
            return None

        soup.extract()  # event was successfully found, we can now safely remove it

        return Event(title, date, "", place, price_range, soup)





