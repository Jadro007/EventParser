import re

import csv
import os
from bs4 import BeautifulSoup

from config import config
from config.config import verbose
from src.dto.Place import Place


class PlaceFinder:
    online_places = ["facebook", "online", "on-line"]
    forbidden_cities = ["Výsluní", "Místo", "Miroslav", "Zájezd", "Česká", "České", "Vysoké", "Vysoká", "Úterý", "Díly",
                        "Košík", "Diváky", "Ostrov", "Řeka", "Pátek", "Hory", "Černá", "Louka", "Veselé", "Železnice",
                        "Lety", "Kruh"]
    regex_for_cities = None

    @staticmethod
    def find(soup) -> [Place]:

        if PlaceFinder.regex_for_cities is None:
            cities = []
            with open(config.ROOT_DIR + os.path.sep + 'data'+os.path.sep+'cities_list.txt', newline='', encoding='utf-8', errors='ignore') as f:
                for city in f:
                    city = city.strip()
                    if city not in PlaceFinder.forbidden_cities:
                        cities.append(re.escape(city))

            cities.extend(PlaceFinder.online_places)
            cities.reverse()  # this is here because the list of cities is ascending and we would not find some cities,
                              # for example Bilov because of Bilovec

            if config.allow_poi:
                with open(config.ROOT_DIR + os.path.sep + 'data'+os.path.sep + 'poi'+os.path.sep +'poi.txt', newline='', encoding='utf-8', errors='ignore') as f:
                    poi = f.readlines()

                poi = [re.escape(x.strip()) for x in poi]
                cities.extend(poi)

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
