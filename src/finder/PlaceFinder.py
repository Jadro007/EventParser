import re

import csv
import os
from bs4 import BeautifulSoup

from config import config
from config.config import verbose
from src.dto.Place import Place


class PlaceFinder:
    forbidden_cities = ["Místo", "Miroslav", "Zájezd", "Česká", "České", "Vysoké", "Vysoká", "Úterý", "Díly", "Košík", "Diváky", "Ostrov", "Řeka", "Pátek", "Hory", "Černá", "Louka", "Veselé"]
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
            cities.extend(["facebook", "online", "on-line"])
            cities.reverse()  # this is here because the list of cities is ascending and we would not find some cities,
                              # for example Bilov because of Bilovec
            regex_for_cities = '|'.join(cities)
            PlaceFinder.regex_for_cities = re.compile(regex_for_cities, flags=re.IGNORECASE)

        if soup.__class__.__name__ == "NavigableString":
            soup = soup.parent

        matched_cities = soup.find_all(text=PlaceFinder.regex_for_cities)

        places = []
        for match in matched_cities:
            result = PlaceFinder.regex_for_cities.search(match)
            city_name = result.group(0)
            # lets check if the place is really there and not as just part of a word
            city_name_regex = re.compile("\\b"+city_name+"\\b", flags=re.IGNORECASE)
            check_for_whole_words = city_name_regex.search(match)
            if check_for_whole_words is None:
                continue
            places.append(Place(city_name, match))

        return places
