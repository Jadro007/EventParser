import re

import csv
import os
from bs4 import BeautifulSoup

from config import config
from config.config import verbose
from src.dto.Place import Place


class PlaceFinder:
    forbidden_cities = ["Místo", "Miroslav", "Zájezd", "Česká", "České", "Vysoké"]
    regex_for_cities = None

    @staticmethod
    def find(soup) -> [Place]:

        if PlaceFinder.regex_for_cities is None:
            cities = []
            with open(config.ROOT_DIR + os.path.sep + 'data'+os.path.sep+'cities.csv', newline='', encoding='utf-8', errors='ignore') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|', )
                for row in spamreader:
                    if row[1] not in PlaceFinder.forbidden_cities:
                        cities.append(row[1])
            regex_for_cities = '|'.join(cities)
            PlaceFinder.regex_for_cities = re.compile(regex_for_cities)

        matched_cities = soup.find_all(text=PlaceFinder.regex_for_cities)
        places = []
        for match in matched_cities:
            result = PlaceFinder.regex_for_cities.search(match)
            places.append(Place(result.group(0), match))

        return places
