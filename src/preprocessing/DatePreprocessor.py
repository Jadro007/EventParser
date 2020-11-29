import re

from typing import Optional

from bs4 import BeautifulSoup
import datetime
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.utils.Utils import Utils


class DatePreprocessor:
    @staticmethod
    def fix_dates(soup):
        # exactly month name (usually this expects shortcuts, like čvn, can can contain dot (.) at the end
        # another supported format is month shortcut with year after it (e.g., čvn. 2020)
        # another supported format is day number in parent element as text and child that contains only month
        # e.g. <a>5<small>říjen</small></a>
        month_regex = "^" + "(\.)*(\s)*(\d{4})*$|^".join(DateFinder.niceMonthNames) + "(\.)*(\s)*(\d{4})*$"
        day_regex = "^" + "(\.)*$|^".join([
            "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "01", "02", "03", "04", "05", "06", "07", "08", "09",
            "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"
        ]) + "$"

        year_regex = "(\d{4})(\.)*"

        month_regex_compiled = re.compile(month_regex, flags=re.IGNORECASE)
        day_regex_compiled = re.compile(day_regex, flags=re.IGNORECASE)
        year_regex_compiled = re.compile(year_regex, flags=re.IGNORECASE)
        month_matches = soup.find_all(text=month_regex_compiled)
        now = datetime.datetime.now()

        for month_match in month_matches:
            parent = month_match.parent.parent

            tmp = parent.getText()

            day_match = parent.find(text=day_regex_compiled)
            day_content = Utils.clean(parent.contents[0])
            year_match = parent.find(text=year_regex_compiled)
            if day_match is not None or day_regex_compiled.search(day_content) is not None:
                if year_match is not None:
                    year_value = year_regex_compiled.search(year_match).group(0)
                    year = year_value.rstrip('.')
                else:
                    year = str(now.year)

                day_value = day_match
                if day_match is None:
                    day_value = day_content
                # if there would be month with year, lets remove the year
                new_date = day_value.rstrip('.') + " " + month_match.rstrip('. 0123456789') + " " + year

                new_date_tag = soup.new_tag("div")
                new_date_tag.string = new_date
                parent.append(new_date_tag)

                print("date fixed from", tmp , "to", new_date)

        return soup


