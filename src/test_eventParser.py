from unittest import TestCase
from bs4 import BeautifulSoup

from src.EventParser import EventParser


class TestEventParser(TestCase):
    def test_parse_single_list_and_single_event(self):
        html = "<html>" \
                   "<body>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li>22.12.2020, Brno, 200 Kč</li>" \
                           "<li>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                       "<div>31.12.2020, Znojmo, 300 Kč</div>" \
                   "</body>" \
               "</html>"

        events = EventParser.parse(html)

        self.assertEqual(events[0].date.realValue, "21.12.2020")
        self.assertEqual(events[0].place.city, "Jihlava")
        self.assertEqual(events[0].priceRange.priceFrom.text, "100 Kč")
        self.assertEqual(events[0].priceRange.priceTo.text, "130 Kč")

        self.assertEqual(events[1].date.realValue, "22.12.2020")
        self.assertEqual(events[1].place.city, "Brno")
        self.assertEqual(events[1].priceRange.priceFrom.text, "200 Kč")
        self.assertEqual(events[1].priceRange.priceTo.text, "200 Kč")

        self.assertEqual(events[2].date.realValue, "23.12.2020")
        self.assertEqual(events[2].place.city, "Praha")
        self.assertEqual(events[2].priceRange.priceFrom.text, "150 Kč")
        self.assertEqual(events[2].priceRange.priceTo.text, "150 Kč")

        self.assertEqual(events[3].date.realValue, "24.12.2020")
        self.assertEqual(events[3].place.city, "Třebíč")
        self.assertEqual(events[3].priceRange, None)

        self.assertEqual(events[4].date.realValue, "31.12.2020")
        self.assertEqual(events[4].place.city, "Znojmo")
        self.assertEqual(events[4].priceRange.priceFrom.text, "300 Kč")
        self.assertEqual(events[4].priceRange.priceTo.text, "300 Kč")

