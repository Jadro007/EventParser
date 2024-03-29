from bs4 import BeautifulSoup
import re

from config import config
from src.dto.Date import Date
from src.dto.Event import Event
from src.dto.Place import Place
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.SingleEventParser import SingleEventParser
from src.utils.Utils import Utils


class ListEventParser:
    @staticmethod
    def parse(soup, dates: [Date], allow_external_place=False, force_place_if_none=None):

        events = []
        # THIS WAS NOT WORKING PROPERLY, REPLACED WITH NEW CODE
        # groups = {}
        # for date in dates:
        #     group_repr = repr(date.group)
        #     if date.group is not None and group_repr not in groups:
        #         groups[group_repr] = date.group
        #
        # for key, group in groups.items():
        #     children = group.container.findChildren()
        #     for child in children:
        #         event = SingleEventParser.parse(child)
        #         if event is not None:
        #             events.append(event)

        # for each date we will try to find event
        date_counter = 0
        date_without_place_counter = 0
        for date in dates:
            # in ListEventParser, we only care about dates that are part of group of dates
            if date.group is None:
                continue
            date_counter += 1
            # Here we will find maximum container, that contains only the one date, but does not contain other dates.
            # This is achieved by having already the event divided into groups, so group.container - 1 length is
            # what we are looking for. So we traverse there from the date to have correct part of the tree.
            previous_parent = None
            parent = date.container
            while parent is not None and Utils.getCustomId(parent) != Utils.getCustomId(date.group.container):
                previous_parent = parent
                parent = parent.parent

            previous_parent = Utils.getTag(previous_parent)

            # if whole page was used as container for the list events event, we need to clone it to prevent messing the HTML structure
            if previous_parent.find("body") is not None:
                previous_parent = BeautifulSoup(str(previous_parent), 'html.parser')

            event = SingleEventParser.parse(previous_parent, date, allow_external_place, force_place_if_none)
            if event == SingleEventParser.NO_PLACE_REASON:
                date_without_place_counter += 1
                continue

            if event is not None:
                events.append(event)

        # for event in events:
        #     # if whole page was used as container for the list events, we do not want to remove it
        #     if event.container.parent is not None:
        #         event.container.extract()  # event was successfully found, we can now safely remove it
        #


        if date_counter == date_without_place_counter and allow_external_place is False:
            return ListEventParser.parse(soup, dates, True, force_place_if_none)

        # This piece of code would force place to events without please for list event.
        # Logic behind this is only one place in all events, other will have the some.
        # However, this has not yet proven really effective and it increases false positive events.
        if config.experimental_force_place_to_all_events_when_same_on_all_events:
            previous_place = None
            all_events_have_same_place = True
            same_place_counter = 0
            for event in events:
                if event.place is None:
                    continue
                same_place_counter += 1
                if previous_place is None or previous_place.city == event.place.city or event.place.city in PlaceFinder.online_places:
                    if event.place.city not in PlaceFinder.online_places:
                        previous_place = event.place
                else:
                    all_events_have_same_place = False
                    break
            if all_events_have_same_place and previous_place is not None and force_place_if_none is None and (same_place_counter > len(events) or date_without_place_counter > same_place_counter):
                return ListEventParser.parse(soup, dates, allow_external_place, previous_place)

        for event in events:
            if event.container.find("body") is None:
                event.container.extract()  # event was successfully found, we can now safely remove it

        return events





