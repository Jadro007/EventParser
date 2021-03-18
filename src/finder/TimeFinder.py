import re

from typing import Optional

from bs4 import BeautifulSoup

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Time import Time
from src.utils.Utils import Utils


class TimeFinder:
    regex_for_time = None

    @staticmethod
    def find(soup) -> Optional[Time]:

        if TimeFinder.regex_for_time is None:
            TimeFinder.regex_for_time = re.compile("((([0-1]?[0-9]|2[0-3]):[0-5][0-9])|([0-1]?[0-9]|2[0-3]) hod)")

        # we try to find all times in the soup using regex
        matched_times = Utils.getTag(soup).find_all(text=TimeFinder.regex_for_time)
        times = []

        # it is possible that there are no times
        if len(matched_times) == 0:
            return None

        # for each time we find, we get valuefrom it
        for match in matched_times:

            # there can be multiple times in one element
            results = TimeFinder.regex_for_time.findall(match)
            for result in results:
                # do not forget that we need to have value as number (int)
                time = result[0]
                if result[3] != "":
                    time = result[3] + ":00"
                times.append(Time(time, match))

        return times
