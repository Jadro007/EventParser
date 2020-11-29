from unittest import TestCase
from bs4 import BeautifulSoup

from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.parser.ListEventParser import ListEventParser
from src.utils.Utils import Utils


class TestListEventParser(TestCase):
    def test_parse_single_list(self):

        html = "<html>" \
                   "<body>" \
                       "<title>This is title</title>" \
                       "<div id=\"group1\">" \
                           "<li><h1>This is h1</h1>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li><h2>This is h2</h2>22.12.2020, Brno, 200 Kč</li>" \
                           "<li><h3>This is h3</h3>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        events = ListEventParser.parse(soup, dates)

        self.assertEqual(events[0].date.dateFrom.realValue, "21.12.2020")
        self.assertEqual(events[0].date.dateTo.realValue, "21.12.2020")
        self.assertEqual(events[0].place.city, "Jihlava")
        self.assertEqual(events[0].priceRange.priceFrom.text, "100 Kč")
        self.assertEqual(events[0].priceRange.priceTo.text, "130 Kč")
        self.assertEqual(events[0].title.value, "This is h1")

        self.assertEqual(events[1].date.dateFrom.realValue, "22.12.2020")
        self.assertEqual(events[1].date.dateTo.realValue, "22.12.2020")
        self.assertEqual(events[1].place.city, "Brno")
        self.assertEqual(events[1].priceRange.priceFrom.text, "200 Kč")
        self.assertEqual(events[1].priceRange.priceTo.text, "200 Kč")
        self.assertEqual(events[1].title.value, "This is h2")

        self.assertEqual(events[2].date.dateFrom.realValue, "23.12.2020")
        self.assertEqual(events[2].date.dateTo.realValue, "23.12.2020")
        self.assertEqual(events[2].place.city, "Praha")
        self.assertEqual(events[2].priceRange.priceFrom.text, "150 Kč")
        self.assertEqual(events[2].priceRange.priceTo.text, "150 Kč")
        self.assertEqual(events[2].title.value, "This is h3")

        self.assertEqual(events[3].date.dateFrom.realValue, "24.12.2020")
        self.assertEqual(events[3].date.dateTo.realValue, "24.12.2020")
        self.assertEqual(events[3].place.city, "Třebíč")
        self.assertEqual(events[3].priceRange, None)
        self.assertEqual(events[3].title.value, "This is title")

