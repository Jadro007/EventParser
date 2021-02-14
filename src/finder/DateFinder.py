import re
import unicodedata

from bs4 import BeautifulSoup

from config.config import verbose
from src.utils.Utils import Utils
from src.dto.Date import Date
import dateparser
import datetime

from src.enhancer.GroupEnhancer import GroupEnhancer


class DateFinder:
    january = ["led", "jan", "january", "leden"]
    february = ["uno", "úno", "feb", "unor", "únor", "february"]
    march = ["bre", "bře", "mar", "brez", "břez", "march", "březen"]
    april = ["dub", "april", "apr", "duben"]
    may = ["kvě", "kve", "květ", "kvet", "květen", "may"]
    june = ["cvc", "čvc", "jun", "červen", "června", "červnu", "červnem", "cerven", "cervna", "cervnu", "cerven",
            "june"]
    july = ["čvn", "cvn", "jul", "červe", "cerve", "červenec", "july"]
    august = ["srp", "srpen", "aug", "august"]
    september = ["zar", "zář", "sep", "září", "zari", "september"]
    october = ["říj", "rij", "říjen", "oct", "october"]
    november = ["lis", "nov", "listopad", "november"]
    december = ["pro", "dec", "prosin", "prosinec", "december"]

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

    separatorRegex = "[\.|\-|\/|\s]\s?"
    dateRegex = "((\d{1,2})" + separatorRegex + "(\d{1,2}|" + regexMonthsNames + ")" + separatorRegex + "(\d{4}))"

    date_regex_compiled = None

    # [^0-9] means not a number, so we do not find same events again
    date_without_year_separator_regex = "[\.|\/]\s?"
    date_without_year_separator_after_month_regex = "[\.|\/|\s]\s?"

    date_without_year_regex = "((\d{1,2})" + date_without_year_separator_regex + "(\d{1,2}|" + regexMonthsNames + ")" + date_without_year_separator_after_month_regex + ")"
    date_without_year_regex_compiled = None

    @staticmethod
    def find(soup, enhance_groups=True):
        dates = []

        now = datetime.datetime.now()

        ##############################################################
        # There is now support for data ranges, that works well for list events.
        # If there are multiple dates in list event container, we treat is as a date range.
        # todo: validate and come with solution for single events
        ##############################################################

        # if verbose > 2:
        #     print("Regex for dates: " + DateFinder.dateRegex)

        ##############################################################
        # todo: there is duplicated almost same logic, refactor this #
        ##############################################################
        if DateFinder.date_regex_compiled is None:
            DateFinder.date_regex_compiled = re.compile(DateFinder.dateRegex, flags=re.IGNORECASE)

        body = soup.find("body")
        if body is not None and body != -1:
            soup = body

        soup = Utils.getTag(soup)

        matches = soup.find_all(text=DateFinder.date_regex_compiled)

        if verbose > 2:
            print("Found dates: ")
            print(matches)

        for match in matches:
            try:
                repr_match = repr(match)
                repr_match = Utils.clean(repr_match)
                specific_dates = DateFinder.date_regex_compiled.findall(repr_match)
            except IndexError:
                continue

            for date in specific_dates:
                real_value = date[0]
                day = date[1]
                month = date[2]
                year = date[3]
                normalised = day + "/" + month + "/" + year
                datetime_value = dateparser.parse(normalised, languages=["cs"])
                if datetime_value is None:
                    if verbose > 2:
                        print("Invalid date", day, month, year)
                    continue

                if datetime_value > datetime.datetime(now.year + 10, now.month, now.day):
                    if verbose > 2:
                        print("Date too much in the future, skipping: ", real_value)
                    continue

                if datetime_value < datetime.datetime(now.year - 10, now.month, now.day):
                    if verbose > 2:
                        print("Date too much in the past, skipping: ", real_value)
                    continue

                dates.append(Date(datetime_value, real_value, match))

        if DateFinder.date_without_year_regex_compiled is None:
            DateFinder.date_without_year_regex_compiled = re.compile(DateFinder.date_without_year_regex,
                                                                     flags=re.IGNORECASE)

        matches = soup.find_all(text=DateFinder.date_without_year_regex_compiled)

        if verbose > 2:
            print("Found dates: ")
            # print(matches)

        for match in matches:
            try:
                repr_match = repr(match)
                repr_match = Utils.clean(repr_match)

                specific_dates = DateFinder.date_without_year_regex_compiled.findall(repr_match)
            except IndexError:
                continue
            except AttributeError:
                continue

            for date in specific_dates:
                real_value = date[0]
                day = date[1]
                month = date[2]
                year = str(now.year)
                normalised = day + "/" + month + "/" + year
                datetime_value = dateparser.parse(normalised, languages=["cs"])
                if datetime_value is None:
                    # if verbose > 2:
                    #     print("Invalid date", day, month, year)
                    continue

                now = datetime.datetime.now()

                if datetime_value > datetime.datetime(now.year + 10, now.month, now.day):
                    if verbose > 2:
                        print("Date too much in the future, skipping: ", real_value)
                    continue

                if datetime_value < datetime.datetime(now.year - 10, now.month, now.day):
                    if verbose > 2:
                        print("Date too much in the past, skipping: ", real_value)
                    continue
                contains_current_date = False
                # When the date was already found previously (with proper year), it is likely to be found here again.
                # In case the event has different year than current year, it would cause to create date range.
                # So we do not check for year to ignore dates like this.
                for already_found_date in dates:
                    if (already_found_date.datetime.month == datetime_value.month
                            and already_found_date.datetime.day == datetime_value.day
                            and already_found_date.container == match
                    ):
                        contains_current_date = True
                        break
                if contains_current_date == False:
                    dates.append(Date(datetime_value, real_value, match, True))

        if enhance_groups:
            GroupEnhancer.set_groups(dates)

        return dates
