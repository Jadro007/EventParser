from bs4 import BeautifulSoup
import re

from src.dto.Date import Date
from src.dto.DateGroup import DateGroup
from src.dto.Place import Place
from src.utils.Utils import Utils


class GroupEnhancer:

    # set groups to dates - useful to determine whether is is single event or list of events
    # if there is only one date in group, it does NOT get set and is kept as None in the date
    # known issues - if there are multiple dates in one element,
    #                it only recognizes the first date (probably not really issue)
    @staticmethod
    def set_groups(dates):

        # here we create initial groups from dates
        # group[0] is list of dates for that group (initially only one date)
        # group[0] is date container (=element) common for dates in the group (initially the date container)
        groups = {}
        for date in dates:
            date.group = None  # remove groups if there are any assigned already
            container_repr = Utils.getCustomId(date.container)
            if container_repr in groups:
                groups[container_repr][0].append(date)
            else:
                groups[container_repr] = [[date], date.container]

        if len(dates) <= 1:  # if there is only one date, we do not care about grouping
            return

        groups = GroupEnhancer.__parse_groups(groups)
        for key, group in groups.items():
            group_dto = DateGroup(group[1], group[0])
            for date in group[0]:
                # we care about groups that have multiple dates
                # If the container is whole page, we should treat it as date without a group
                if len(group[0]) > 1 and group[1].find("html") is None and group[1].parent.find("body") is None:
                    date.set_group(group_dto)

    @staticmethod
    def __parse_groups(groups):
        # in this function, we recursively traverse up the HTML document,
        # trying to find common parents for date containers
        should_end = False
        for key, group in groups.copy().items():

            if group[1].parent is None:
                should_end = True
                continue

            does_group_contains_more_events_with_different_parents = False
            for date in group[0]:
                for date2 in group[0]:
                    if date != date2 and date.container != date2.container:
                        does_group_contains_more_events_with_different_parents = True


            if len(group[0]) > 2 and does_group_contains_more_events_with_different_parents:
                # if the group contains more date, we are happy with that group and leave it as is
                # but the dates must have different parent element
                continue

            parent = group[1].parent
            parent_repr = Utils.getCustomId(parent)
            if parent_repr in groups:  # for each group, we check if parent is already existing
                groups[parent_repr][0].extend(group[0]) # if yes, we add all dates from our group
                del groups[Utils.getCustomId(group[1])]
            else:
                groups[parent_repr] = group # if this is first occurrence of the parent, we move the group there
                del groups[Utils.getCustomId(group[1])]
                group[1] = parent

        is_finished = True # all groups are finished once there are more then one date in each group
        for key, group in groups.items():
            does_group_contains_more_events_with_different_parents = False
            for date in group[0]:
                for date2 in group[0]:
                    if date != date2 and date.container != date2.container:
                        does_group_contains_more_events_with_different_parents = True
            if len(group[0]) <= 2 or does_group_contains_more_events_with_different_parents == False:
                is_finished = False


        # if there would be just one date in the group, it works fine thanks to bs4 magic
        # on line 36 (parent = group[1].parent)
        # For some (to me yet unknown reason), HTML element parent is the same, so it gets recognized as known group
        # and then it gets deleted (lines 38-40)
        # Plus there are now added should_end and is parent None

        if is_finished or should_end:
            return groups

        return GroupEnhancer.__parse_groups(groups)


