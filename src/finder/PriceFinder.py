import re

from typing import Optional

from bs4 import BeautifulSoup

from src.dto.PriceRange import PriceRange
from src.dto.Price import Price


class PriceFinder:
    regex_for_price = None

    @staticmethod
    def find(soup) -> Optional[PriceRange]:

        if PriceFinder.regex_for_price is None:
            PriceFinder.regex_for_price = re.compile("((\d+)\s*(kc|kč|Kč|,-))")

        # we try to find all prices in the soup using regex
        matched_prices = soup.find_all(text=PriceFinder.regex_for_price)
        prices = []

        # it is possible that there are no prices
        if len(matched_prices) == 0:
            return None

        # for each price we find, we get value, text and currency from it
        for match in matched_prices:

            # there can be multiple prices in one element
            results = PriceFinder.regex_for_price.findall(match)
            for result in results:
                # do not forget that we need to have value as number (int)
                prices.append(Price(int(result[1]), result[0], result[2], match))

        # if there was one result, we return it as PriceRange with same from and to values
        if len(prices) == 1:
            return PriceRange(prices[0], prices[0], prices[0].container)

        # if there are multiple results, we want to know the price range, so lets sort it by value
        prices.sort(key=lambda price: price.value, reverse=False)

        # and return PriceRange with the first and last price
        return PriceRange(prices[0], prices[-1], prices[0].container)
