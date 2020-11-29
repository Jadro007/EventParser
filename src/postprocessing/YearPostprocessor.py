import re

from typing import Optional

from bs4 import BeautifulSoup
import datetime
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.utils.Utils import Utils


class YearPostprocessor:
    year_regex_compiled = re.compile("(\d{4})")


    @staticmethod
    def fix_year(events):
        # Some events have guessed year when its date was found without a year
        # This will try to find proper year for that date
        # Current implementation will check if there is any year in the event title and use that instead if present
        # note: if there are multiple years, we will take the newest one
        for event in events:
            fixed_year = None
            if event.date.dateFrom.isYearGuessed or event.date.dateTo.isYearGuessed:
                title = event.title.value
                matches = YearPostprocessor.year_regex_compiled.findall(title)
                fixed_year = None
                for new_year in matches:
                    if fixed_year is None or new_year > fixed_year:
                        fixed_year = new_year

            if fixed_year is not None:
                if event.date.dateFrom.isYearGuessed:
                    new_datetime = datetime.datetime(
                        event.date.dateFrom.datetime.year + 1,
                        event.date.dateFrom.datetime.month,
                        event.date.dateFrom.datetime.day
                    )

                    event.date.dateFrom.datetime = new_datetime

                if event.date.dateTo.isYearGuessed:
                    new_datetime = datetime.datetime(
                        event.date.dateTo.datetime.year + 1,
                        event.date.dateTo.datetime.month,
                        event.date.dateTo.datetime.day
                    )

                    event.date.dateTo.datetime = new_datetime





