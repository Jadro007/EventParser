import re

from typing import Optional
import urllib.parse

from bs4 import BeautifulSoup

from src import utils
from src.dto.Description import Description
from src.dto.Event import Event
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.utils.Utils import Utils


class TargetUrlFinder:

    @staticmethod
    def add_target_url(events, url) -> [Event]:

        for event in events:
            target_url = None

            for a in event.title.container.find_all("a"):
                target_url = TargetUrlFinder._get_url_from_href(a.get("href"), url)
                if target_url is not None:
                    break

            if target_url is None:
                common_container = event.small_container
                if common_container is None:
                    common_container = event.container

                for a in common_container.find_all("a"):
                    target_url = TargetUrlFinder._get_url_from_href(a.get("href"), url)
                    if target_url is not None:
                        break

            event.target_url = target_url

        return events

    @staticmethod
    def _get_url_from_href(href, url):
        if href is None:
            return None
        if href.lstrip().startswith('#'):
            return None
        if href.lstrip().startswith('mailto'):
            return None
        if href.lstrip().startswith('javascript'):
            return None

        base_url = TargetUrlFinder._base_url(url)

        href = href.lstrip(" .")

        if href.startswith("http"):
            target_url = href
        elif href == "/":
            target_url = base_url
        elif href.startswith("/"):
            target_url = base_url + href
        else:
            target_url = base_url + href

        if TargetUrlFinder._base_url(target_url) != base_url:
            return None

        return target_url

    @staticmethod
    def _base_url(url):
        parsed = urllib.parse.urlparse(url)
        path = ""
        parsed = parsed._replace(path=path)
        parsed = parsed._replace(params='')
        parsed = parsed._replace(query='')
        parsed = parsed._replace(fragment='')
        return parsed.geturl()