import re

from typing import Optional

from bs4 import BeautifulSoup

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title


class TitleFinder:
    @staticmethod
    def find(soup) -> Optional[Title]:

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


