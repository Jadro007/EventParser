import re

from typing import Optional

from bs4 import BeautifulSoup

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.utils.Utils import Utils


class TitleFinder:
    @staticmethod
    def find(soup, is_single_event=False) -> Optional[Title]:
        if is_single_event:
            return TitleFinder._find_internal_single_event(soup)

        return TitleFinder._find_internal(soup, True)

    @staticmethod
    def _find_internal(soup, recursive):
        title = soup.find(["h1"], recursive=recursive)
        if title is None:
            title = soup.find("h2", recursive=recursive)
            if title is None:
                title = soup.find("h3", recursive=recursive)
                if title is None:
                    title = soup.find("h4", recursive=recursive)

        # Traverse up (when traversing up, we want to try find title only in direct children, not in all structure.
        # That could accidentally get title from other event.
        if title is None and soup.parent is not None:
            return TitleFinder._find_internal(soup.parent, False)

        if title is None:
            title = soup.find("title")

        if title is None:
            return None

        text = title.getText()

        return Title(text, title)


    @staticmethod
    def _find_internal_single_event(soup):
        container = soup
        parent = soup.parent
        while parent is not None:
            container = parent
            parent = parent.parent

        titles = container.find_all(["h1", "h2", "h3", "h4"])

        lowest_score = 999
        title = None
        for t in titles:
            score = Utils.get_depth(t)
            if t.name == "h1":
                score += 1
            if t.name == "h2":
                score += 2
            if t.name == "h3":
                score += 3
            if t.name == "h4":
                score += 4

            if score < lowest_score and t.getText() is not "":
                lowest_score = score
                title = t

        if title is None:
            title = soup.find("title")

        if title is None:
            return None

        text = title.getText()

        return Title(text, title)
