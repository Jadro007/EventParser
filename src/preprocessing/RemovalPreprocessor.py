import re

from typing import Optional

from bs4 import BeautifulSoup, Comment, Doctype
import datetime
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.utils.Utils import Utils


class RemovalPreprocessor:
    @staticmethod
    def cleanup(soup):
        RemovalPreprocessor.remove_comments(soup)
        RemovalPreprocessor.remove_script_and_style_tag(soup)
        RemovalPreprocessor.remove_fake_dates(soup)

        return soup

    @staticmethod
    def unwrap(soup):
        for element in soup.find_all(["small", "b", "i", "u", "big"]):
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
        [x.extract() for x in soup.findAll(attrs={"class": "post-date"})]
        # for item in soup.contents:
        #     if isinstance(item, Doctype):
        #         item.extract()
        return soup

    @staticmethod
    def remove_fake_dates(soup):
        fake_dates = [
                        "Vytvořeno", "Poslední aktualizace", "Naposledy změněno", "Dnes je", "Publikováno",
                        "Vloženo", "Počasí dnes", "svátek má", "Zveřejněno"
                        ]

        regex_for_fake_dates = '|'.join(fake_dates)
        regex_for_fake_dates_compiled = re.compile(regex_for_fake_dates, flags=re.IGNORECASE)

        matched_fake_dates = soup.find_all(text=regex_for_fake_dates_compiled)
        for match in matched_fake_dates:
            if len(DateFinder.find(match, False)) == 0:
                Utils.getTag(match).parent.extract()
            else:
                match.extract()
        return soup
