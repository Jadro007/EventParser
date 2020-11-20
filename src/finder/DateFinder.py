import re

from bs4 import BeautifulSoup

from config.config import verbose
from src.dto.Date import Date
import dateparser

from src.enhancer.GroupEnhancer import GroupEnhancer


class DateFinder:
    january = ["led\.", "led", "january"]
    february = ["unor", "únor", "february"]
    march = ["brez", "břez", "march"]
    april = ["dub", "april"]
    may = ["květ", "kvet", "may"]
    june = ["červen", "června", "červnu", "červnem", "cerven", "cervna", "cervnu", "cerven", "june"]
    july = ["červe", "cerve", "july"]
    august = ["srp", "august"]
    september = ["září", "zari", "september"]
    october = ["Říj\.", "říj", "rij", "october"]
    november = ["listopad", "november"]
    december = ["prosin", "december"]

    niceMonthNames = [
        *january,
        *february,
        *march,
        *april,
        *may,
        *june,
        *july,
        *august,
        *september,
        *october,
        *november,
        *december
    ]

    regexMonthsNames = "[a-z]*|".join(niceMonthNames) + "[a-z]*"

    separatorRegex = "[\.|\-|/|\s]\s?"
    dateRegex = "((\d{1,2})" + separatorRegex + "(\d{1,2}|"+regexMonthsNames+")" + separatorRegex + "(\d{4}))"

    @staticmethod
    def find(soup):
        dates = []
        if verbose > 2:
            print("Regex for dates: " + DateFinder.dateRegex)

        date_regex_compiled = re.compile(DateFinder.dateRegex, flags=re.IGNORECASE)

        matches = soup.find_all(text=date_regex_compiled)

        if verbose > 2:
            print("Matched dates: ")
            print(matches)

        for match in matches:

            parsed = date_regex_compiled.findall(repr(match))[0]

            real_value = parsed[0]
            day = parsed[1]
            month = parsed[2]
            year = parsed[3]
            normalised = day + "/" + month + "/" + year
            datetime = dateparser.parse(normalised, languages=["cs"])

            dates.append(Date(datetime, real_value, match))

        GroupEnhancer.set_groups(dates)

        return dates