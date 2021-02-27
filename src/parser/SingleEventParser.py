from bs4 import BeautifulSoup, NavigableString
import re

from config import config
from config.config import verbose
from src.dto.DateRange import DateRange
from src.dto.Event import Event
from src.dto.Place import Place
from src.finder.PriceFinder import PriceFinder
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.finder.TitleFinder import TitleFinder
from src.utils.Utils import Utils



class SingleEventParser:
    NO_PLACE_REASON = 'no-place'

    @staticmethod
    def parse(soup, date, allow_external_place=False, force_place_if_none=None):

        is_single_event = not date.group
        date_container = date.container

        # todo: support multiple dates events (including date range)
        if is_single_event is True:
            try:
                # For single event, soup is whole page (not sure if that is useful really).
                # So we limit finding other dates close to the main date (to prevent creating range with some random dates on page)
                if date_container.parent is not None:
                    date_container = date.container.parent
                if date_container.parent is not None:
                    date_container = date.container.parent

                dates = DateFinder.find(date_container, False)
            except AttributeError:
                return
        else:
            try:
                dates = DateFinder.find(soup, False)
            except AttributeError:
                return

        # todo: fix date range when last date overlaps to next year
        #       currently it would just swap the dates here, we should prefer the order of dates in html structure
        first_date = date
        last_date = date
        for d in dates:
            if d.datetime < first_date.datetime and date.container.parent.sourceline - d.container.parent.sourceline < 20:
                first_date = d
            if d.datetime > last_date.datetime and date.container.parent.sourceline - d.container.parent.sourceline < 20:
                last_date = d

        # if event is in different year than current year, we might have guessed the year wrong, so if day and month match, lets ignore it
        if last_date.isYearGuessed == True and first_date.datetime.day == last_date.datetime.day and first_date.datetime.month == last_date.datetime.month:
            last_date = first_date

        # try to find place that is closest to the date
        # todo: write test for it
        places = PlaceFinder.find(date_container)
        if len(places) == 0:
            places = PlaceFinder.find(soup)
        place = None
        sourceline_diff = 999999
        if isinstance(date.container, NavigableString):
            date_sourceline = date.container.parent.sourceline
        else:
            date_sourceline = date.container.sourceline

        for p in places:
            if isinstance(p.container, NavigableString):
                place_sourceline = p.container.parent.sourceline
            else:
                place_sourceline = p.container.sourceline

            diff = abs(place_sourceline - date_sourceline)
            if diff < sourceline_diff:
                sourceline_diff = diff
                place = p

        # Some websites do not have location, because they present specific venue.
        # This could be improved by further investigating other pages of the website (e.g. contact or about page)
        # Here we try to find some location in some places where it could be (e.g. title), however it lowers scoring.
        # This only happens when all events do not have place to correctly eliminate false positive events.
        if place is None and allow_external_place:
            previous_parent = date.container
            parent = date.container
            while parent is not None:
                previous_parent = parent
                parent = parent.parent

            website_title = previous_parent.find("title")
            if website_title is not None:
                places = PlaceFinder.find(website_title)
                if len(places) > 0:
                    place = places[0]
                    place.is_external_place = True

            if place is None and config.allow_place_from_footer:
                website_footer = previous_parent.find("footer")
                if website_footer is not None:
                    places = PlaceFinder.find(website_footer)
                    for p in places:
                        if p.city.lower() == "facebook":
                            continue
                        place = p
                        place.is_external_place = True
                        break

        if place is None and force_place_if_none is not None:
            place = Place(force_place_if_none.city, force_place_if_none.container)
            place.is_forced = True

        if place is None:

            if verbose > 2:
                print("Found event without place with date: " + date.realValue + ", skipping")
            return SingleEventParser.NO_PLACE_REASON



        price_range = PriceFinder.find(soup)

        # we want to be able to find the most relevant title for event, so we will start with container that contains
        # both date and place, so there is quite chance there will be also the title
        title = None
        if is_single_event:
            container = Utils.lowest_common_ancestor(date.container, place.container)
            if container is None:
                return None
            container = container.parent
            title = TitleFinder.find(container, is_single_event, [first_date.container, place.container])
        else:
            container = soup
            title = TitleFinder.find(container, is_single_event, [first_date.container, place.container])
            if title is None and date.container == place.container and soup.parent is not None:
                container = soup.parent
                title = TitleFinder.find(container, is_single_event, [first_date.container, place.container])
            # in case that date and place are in the same container, it might happen that title will not be there,
            # so we increase search container to parent

        if title is None:
            if verbose > 2:
                print("Found event without title (date: " + date.realValue + ", place: " + place.city + "), skipping")
            return None

        # if container is not None and container.sourceline is not None and title.container is not None and container.sourceline - title.container.sourceline > 150:
        #     if verbose > 2:
        #         print("Found event with title too far (title: " + title.value + ",date: " + date.realValue + ", place: " + place.city + "), skipping")
        #     return None

        # we cannot remove the event, because it could break selectors created for Selenium
        if config.allow_selenium is False:
             soup.extract()  # event was successfully found, we can now safely remove it

        return Event(title, DateRange(first_date, last_date, soup), "", place, price_range, soup)





