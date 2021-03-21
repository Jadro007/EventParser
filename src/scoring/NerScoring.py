import re

from typing import Optional

from bs4 import BeautifulSoup, NavigableString
import datetime

from config import config
from src.dto.Description import Description
from src.dto.Event import Event
from src.dto.PriceRange import PriceRange
from src.dto.Price import Price
from src.dto.Title import Title
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.utils.Utils import Utils
import subprocess
import tempfile


class NerScoring:
    regex_for_ner_class = None

    valid_classes = ["hudb", "hudeb", "festiv", "koncert", "sport", "opera", "opery", "fotbal", "orchestr",
                     "kulturní_události", "budoucí_události", "budoucí_sportovní_události", "rap", "rock", "metal",
                     "pop", "country", "koncert", "tenis", "hokej", "olympiada", "mistrovství", "volejbal",
                     "brusleni", "judo", "basketbal", "jazz", "kultura", ]

    @staticmethod
    def score_events(events: [Event]):

        if config.allow_poi is False:
            return events

        if NerScoring.regex_for_ner_class is None:
            NerScoring.regex_for_ner_class = re.compile('class="([^"]+)"')

        processes = []

        for event in events:
            content = event.title.value + " " + event.place.city + " " + event.description.value
            content = content[0:200]
            f = tempfile.TemporaryFile()

            params = ['timeout', '10', 'python', "wikiNE.py", '-t', content.encode("utf-8")]

            p = subprocess.Popen(params,
                                 cwd=config.ROOT_DIR + "/nlp/ner/",
                                 stdout=f,
                                 stderr=f
                                 )
            processes.append((p, f, event))

        for p, f, event in processes:
            p.wait()
            f.seek(0)

            result_xml = f.read().decode("utf-8")
            matches = NerScoring.regex_for_ner_class.findall(result_xml)

            ner_classes = " ".join(matches)
            found_valid = 0
            for valid_class in NerScoring.valid_classes:
                if valid_class in ner_classes:
                    found_valid += 1

            event.score += min(30, found_valid * 5)

            event_classes = []
            for ner_class in ner_classes.lower().split(" "):
                event_classes.append(ner_class[1:])

            event.tags = event_classes

        return events
