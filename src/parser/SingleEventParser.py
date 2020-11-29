from bs4 import BeautifulSoup
import re

from config.config import verbose
from src.dto.DateRange import DateRange
from src.dto.Event import Event
from src.finder.PriceFinder import PriceFinder
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.finder.TitleFinder import TitleFinder
from src.utils.Utils import Utils


class SingleEventParser:

    @staticmethod
    def parse(soup, date):

        is_single_event = not date.group

        # todo: support multiple dates events (including date range)
        try:
            dates = DateFinder.find(soup, False)
        except AttributeError:
            return

        first_date = date
        last_date = date
        for d in dates:
            if d.datetime < first_date.datetime:
                first_date = d
            if d.datetime > last_date.datetime:
                last_date = d

        # try to find place that is closest to the date
        # Currently it just checks depth
        # todo: Could be improved by checking closeness in HTML structure
        # todo: write test for it
        places = PlaceFinder.find(soup)
        date_depth = Utils.get_depth(date.container)
        depth_diff = 999999
        place = None
        for p in places:
            diff = abs(Utils.get_depth(p.container) - date_depth)
            if diff < depth_diff:
                depth_diff = diff
                place = p

        if place is None:
            if verbose > 2:
                print("Found event without place with date: " + date.realValue + ", skipping")
            return None

        price_range = PriceFinder.find(soup)

        # we want to be able to find the most relevant title for event, so we will start with container that contains
        # both date and place, so there is quite chance there will be also the title
        if is_single_event:
            container = Utils.lowest_common_ancestor(date.container, place.container).parent
        else:
            container = soup

        title = TitleFinder.find(container, is_single_event)
        if title is None:
            if verbose > 2:
                print("Found event without title (date: " + date.realValue + ", place: " + place.city + "), skipping")
            return None

        soup.extract()  # event was successfully found, we can now safely remove it

        return Event(title, DateRange(first_date, last_date, soup), "", place, price_range, soup)





