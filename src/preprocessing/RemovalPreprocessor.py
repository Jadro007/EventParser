import re

from typing import Optional

from bs4 import BeautifulSoup, Comment, Doctype
import datetime
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder


class RemovalPreprocessor:
    @staticmethod
    def remove_comments(soup):
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        return soup
    @staticmethod

    def remove_script_and_style_tag(soup):
        [x.extract() for x in soup.findAll(['script', 'style'])]
        # for item in soup.contents:
        #     if isinstance(item, Doctype):
        #         item.extract()
        return soup
