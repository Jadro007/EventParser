from bs4 import BeautifulSoup
import re

from config.config import verbose
from src.dto.Event import Event
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder


class SingleEventParser:

    @staticmethod
    def parse(soup):

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

        soup.extract()  # event was successfully found, we can now safely remove it

        return Event("", date, "", place, 0, soup)





