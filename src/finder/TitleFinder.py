import re

from typing import Optional

from bs4 import BeautifulSoup

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.utils.Utils import Utils


class TitleFinder:

    title_blacklist = ["Odběr novinek", "Nejbližší uvedení", "Říjen", "všechnapředstavení", "Menu", "Hledání", "Podrobné nastavení", "Back Button Back", "Vaše soukromí", "Více informací", "Koncerty", "Připravované koncerty", "kapela", "Back to the top"]

    @staticmethod
    def find(soup, is_single_event=False) -> Optional[Title]:
        if is_single_event:
            return TitleFinder._find_internal_single_event(soup)

        # sometimes list events do not have proper title
        # so if the event container is content of main title, it is likely name of the event
        # todo: this operation is quite resource heavy, might be good idea to cache it for each site
        main_title = TitleFinder._find_internal_single_event(soup)
        use_main_title = False
        if main_title is not None:
            main_title_regex_compiled = re.compile(main_title.value, flags=re.IGNORECASE)
            if soup.find(text=main_title_regex_compiled) is not None:
                use_main_title = True

        title_from_list = TitleFinder._find_internal(soup, True)
        if use_main_title:
            title_from_list.alternative_value = main_title.value

        return title_from_list

    @staticmethod
    def _find_internal(soup, recursive):
        title = soup.find(["h1"], recursive=recursive)
        if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
            title = soup.find("h2", recursive=recursive)
            if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                title = soup.find("h3", recursive=recursive)
                if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                    title = soup.find("h4", recursive=recursive)
                    if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "" or TitleFinder.__title_contains_only_date(title):
                        # for list event, it is possible to contain link to event and usually there is either
                        # event name (we want that) or just url (we do not want that)
                        link = soup.find("a", recursive=recursive)
                        if link is not None and "www" not in link.getText() and ".cz" not in link.getText() and "http" not in link.getText() and Utils.clean(link.getText()) != "" and TitleFinder.__title_contains_only_date(link) is False:
                            title = link

        # Traverse up (when traversing up, we want to try find title only in direct children, not in all structure.
        # That could accidentally get title from other event.
        if (title is None or title.getText() in TitleFinder.title_blacklist) and soup.parent is not None:
            return TitleFinder._find_internal(soup.parent, False)

        if title is None or title.getText() in TitleFinder.title_blacklist or Utils.clean(title.getText()) == "":
            title = soup.find("title")

        if title is None or title.getText() in TitleFinder.title_blacklist:
            return None

        text = Utils.clean(title.getText())
        aleternative_text = ""
        if len(text) < 50:
            container = soup
            parent = soup.parent
            while parent is not None:
                container = parent
                parent = parent.parent
            h1 = container.find(["h1"], recursive=recursive)
            if h1 is not None and h1.getText() not in TitleFinder.title_blacklist and Utils.clean(h1.getText()) != "":
                aleternative_text = Utils.clean(h1.getText()) + " - " + text

        return Title(text, aleternative_text, title)

    @staticmethod
    def __title_contains_only_date(title):
        text = title.getText()
        if len(text) < 5:
            return False
        dates = DateFinder.find(title)
        for date in dates:
            text = text.replace(date.realValue, "")

        text = Utils.clean(text)
        if len(text) < 5:
            return True

        return False


    @staticmethod
    def _find_internal_single_event(soup):
        sibling = soup.find_next_sibling()
        if sibling is not None:
            soup_next_sibling_sourceline = sibling.sourceline
        else:
            soup_next_sibling_sourceline = 999999
        container = soup
        parent = soup.parent
        while parent is not None:
            container = parent
            parent = parent.parent

        titles = container.find_all(["h1", "h2", "h3", "h4"])

        lowest_score = 999
        title = None
        for t in titles:
            # we are only interested in headings before the container, that is achieved by calculating the
            # sourceline of next sibling to the soup
            if t.sourceline > soup_next_sibling_sourceline:
                continue

            if Utils.clean(t.getText()) in TitleFinder.title_blacklist or Utils.clean(t.getText()) == "":
                continue

            score = Utils.get_depth(t)
            if t.name == "h1":
                score += 1
            if t.name == "h2":
                score += 5
            if t.name == "h3":
                score += 10
            if t.name == "h4":
                score += 15

            if score < lowest_score and t.getText() is not "":
                lowest_score = score
                title = t

        if title is None:
            title = soup.find("title")

        if title is None:
            return None

        text = Utils.clean(title.getText())

        return Title(text, "", title)
