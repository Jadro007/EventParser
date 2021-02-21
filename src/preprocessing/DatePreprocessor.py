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

    @staticmethod
    def prepare_date_ranges(soup):
        # and also prepare date ranges with different months
        # e.g. 13.10.-15.11. 2021

        date_range_with_different_months_regex = DateFinder.date_without_year_regex + "\s?\-\s?" + DateFinder.dateRegex

        print(date_range_with_different_months_regex)

        date_range_regex_with_different_months_compiled = re.compile(date_range_with_different_months_regex, flags=re.IGNORECASE)
        date_range_matches = soup.find_all(text=date_range_regex_with_different_months_compiled)
        for date_range_match in date_range_matches:
            match = date_range_regex_with_different_months_compiled.search(date_range_match)
            range_text = match.group(0)
            from_date_day_and_month = match.group(1)
            year = match.group(7)
            to_date_text = match.group(4)
            fixed_text = date_range_match.replace(range_text, from_date_day_and_month + year + "##" + to_date_text)
            date_range_match.replace_with(fixed_text)
            print("PREPARED DATE RANGE " + fixed_text)

        # we want to also prepare date ranges here
        # e.g., 13.-17. 9. 2021
        # note: that [\-|–] "-" (dash) and "–" (hyphen) are two different signs (which is fun to debug)
        date_range_regex = "(\d{1,2})" + DateFinder.separatorRegex + "\s?[\-|–]\s?" + DateFinder.dateRegex
        print(date_range_regex)

        date_range_regex_compiled = re.compile(date_range_regex, flags=re.IGNORECASE)
        date_range_matches = soup.find_all(text=date_range_regex_compiled)
        for date_range_match in date_range_matches:
            match = date_range_regex_compiled.search(date_range_match)
            range_text = match.group(0)

            # this is fix for case of 1.2.2020 - 2.2.2021 - it finds 20 - 2.2.2021 as a date range by accident,
            # so we check whether before the date range is number - if yes, it was part of other date a we ignore it
            # match_position > 0 ignores when not found or it starts with the match
            match_position = date_range_match.find(range_text)
            if match_position > 0 and date_range_match[match_position - 1].isnumeric() == True:
                continue

            from_date_day = match.group(1)
            to_date_text = match.group(2)
            to_date_day = match.group(3)

            from_date_text = from_date_day + to_date_text.lstrip(to_date_day)

            fixed_text = date_range_match.replace(range_text, from_date_text + "##" + to_date_text)
            date_range_match.replace_with(fixed_text)
            print("PREPARED DATE RANGE " + fixed_text)

        return soup

    @staticmethod
    def fix_today_and_tomorrow(soup_str):
        today = datetime.datetime.now()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        soup_str = soup_str.replace("dnes", str(today.day) + ". " + str(today.month) + ". " + str(today.year))
        soup_str = soup_str.replace("zítra", str(tomorrow.day) + ". " + str(tomorrow.month) + ". " + str(tomorrow.year))

        return soup_str
