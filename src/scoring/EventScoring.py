import re

from typing import Optional

from bs4 import BeautifulSoup, NavigableString
import datetime

from src.dto.Event import Event
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.utils.Utils import Utils


class EventScoring:
    @staticmethod
    def score_events(events: [Event]):

        for event in events:
            event.score = 100

            if event.date.dateFrom.isYearGuessed:
                event.score -= 10

            if event.date.dateTo.isYearGuessed:
                event.score -= 10

            # here we evaluate general closeness of date and place - the more far away, the more minus points
            if event.date.container != event.place.container and event.place.is_external_place is False and event.place.is_forced is False:
                if isinstance(event.date.dateFrom.container, NavigableString):
                    date_sourceline = event.date.dateFrom.container.parent.sourceline
                else:
                    date_sourceline = event.date.dateFrom.container.sourceline

                if date_sourceline is None:
                    date_sourceline = 0

                if isinstance(event.place.container, NavigableString):
                    place_sourceline = event.place.container.parent.sourceline
                else:
                    place_sourceline = event.place.container.sourceline

                if place_sourceline is None:
                    place_sourceline = 0

                sourceline_diff = abs(date_sourceline - place_sourceline)
                event.score -= sourceline_diff / 10

            # external place can be unrelated to the event, so we lower score
            if event.place.is_external_place is True:
                event.score -= 20

            # forced place can be unrelated to the event, so we lower score
            if event.place.is_forced is True:
                event.score -= 40

            # if list event has as container whole page, it is not really reliable
            if event.date.dateFrom.group is not None and event.date.container.html is not None:
                event.score -= 30

            # for single events (not in lists)
            if event.date.dateFrom.group is None:
                diff = abs(Utils.getTag(event.date.dateFrom.container).sourceline - Utils.getTag(event.title.container).sourceline)
                if diff > 25:
                    event.score -= min(diff - 25, 60)

            if event.place.city.lower() in PlaceFinder.online_places:
                event.score -= 10

            # is something is moved or cancelled, it is likely to be event
            if (
                "zrušeno" in event.title.value.lower() or "přesunuto" in event.title.value.lower() or
                "zrušeno" in event.title.alternative_value.lower() or "přesunuto" in event.title.alternative_value.lower()
            ):
                event.score += 15

            if event.score > 100:
                event.score = 100

            if event.score < 0:
                event.score = 0

            # other ideas - add score for having time close to date
            # other ideas - add score for having price

        return events

