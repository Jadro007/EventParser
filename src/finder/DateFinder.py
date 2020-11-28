import re

from bs4 import BeautifulSoup

from config.config import verbose
from src.dto.Date import Date
import dateparser
import datetime

from src.enhancer.GroupEnhancer import GroupEnhancer


class DateFinder:
    january = ["led", "jan", "january"]
    february = ["uno", "úno", "feb", "unor", "únor", "february"]
    march = ["bre", "bře", "mar", "brez", "břez", "march"]
    april = ["dub", "april", "apr"]
    may = ["kvě", "kve", "květ", "kvet", "may"]
    june = ["cvc", "čvc", "jun", "červen", "června", "červnu", "červnem", "cerven", "cervna", "cervnu", "cerven", "june"]
    july = ["čvn", "cvn", "jul", "červe", "cerve", "july"]
    august = ["srp", "aug", "august"]
    september = ["zar", "zář", "sep", "září", "zari", "september"]
    october = ["říj", "rij", "oct", "october"]
    november = ["lis", "nov", "listopad", "november"]
    december = ["pro", "dec", "prosin", "december"]

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

    date_regex_compiled = None

    @staticmethod
    def find(soup):
        dates = []
        # if verbose > 2:
        #     print("Regex for dates: " + DateFinder.dateRegex)

        if DateFinder.date_regex_compiled is None:
            DateFinder.date_regex_compiled = re.compile(DateFinder.dateRegex, flags=re.IGNORECASE)

        matches = soup.find_all(text=DateFinder.date_regex_compiled)

        if verbose > 2:
            print("Found dates: ")
            print(matches)

        for match in matches:
            # todo: support multiple dates in one match (including daterange)
            parsed = DateFinder.date_regex_compiled.findall(repr(match))[0]

            real_value = parsed[0]
            day = parsed[1]
            month = parsed[2]
            year = parsed[3]
            normalised = day + "/" + month + "/" + year
            datetime_value = dateparser.parse(normalised, languages=["cs"])
            if datetime_value is None:
                if verbose > 2:
                    print("Invalid date", day, month, year)
                continue

            now = datetime.datetime.now()

            if datetime_value > datetime.datetime(now.year + 10, now.month, now.day):
                if verbose > 2:
                    print("Date too much in the future, skipping: ", real_value)
                continue

            dates.append(Date(datetime_value, real_value, match))

        GroupEnhancer.set_groups(dates)

        return dates