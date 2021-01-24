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
    def cleanup(soup):
        RemovalPreprocessor.remove_comments(soup)
        RemovalPreprocessor.remove_script_and_style_tag(soup)

        return soup

    @staticmethod
    def unwrap(soup):
        for element in soup.find_all(["small", "span", "b", "strong", "i", "u", "big"]):
            parent = element.parent
            try:
                element.unwrap()
                if parent is None and parent.getChilren() == 0:
                    new_text = re.sub(r'\n\s*\n', r'\n\n', parent.getText().strip(), flags=re.M)
                    parent.string = new_text
            except ValueError:
                pass
        return soup

    @staticmethod
    def remove_comments(soup):
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        return soup
    @staticmethod

    def remove_script_and_style_tag(soup):
        [x.extract() for x in soup.findAll(['script', 'style', 'br'])]
        [x.extract() for x in soup.findAll(attrs={"role": "dialog"})]
        # for item in soup.contents:
        #     if isinstance(item, Doctype):
        #         item.extract()
        return soup
