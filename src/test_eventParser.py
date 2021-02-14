from unittest import TestCase
from bs4 import BeautifulSoup

from src.EventParser import EventParser


class TestEventParser(TestCase):
    def test_parse_single_list_and_single_event(self):

        html = "<html>" \
                   "<head><title>This is title</title></head>" \
                   "<body>" \
                       "<div><h1>This is parent h1</h1><div id=\"group1\">" \
                           "<li><h1>This is h1</h1>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li><h2>This is h2</h2>22.12.2020, Brno, 200 Kč</li>" \
                           "<li><h3>This is h3</h3>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div>" \
                       "<div>" \
                       "<li>26.12.2020, Mikulov, 500 Kč</li>" \
                       "<li>27.12.2020, Lednice</li>" \
                       "<li>29.12.2020, Hustopeče</li>" \
                       "</div>" \
                       "<div>30.12.2020 - 31.12.2020, Znojmo, 300 Kč</div>" \
                   "</body>" \
               "</html>"
        events = EventParser.parse(html)

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
        self.assertEqual(events[1].title.value, "This is h1")

        self.assertEqual(events[2].date.dateFrom.realValue, "23.12.2020")
        self.assertEqual(events[2].date.dateTo.realValue, "23.12.2020")
        self.assertEqual(events[2].place.city, "Praha")
        self.assertEqual(events[2].priceRange.priceFrom.text, "150 Kč")
        self.assertEqual(events[2].priceRange.priceTo.text, "150 Kč")
        self.assertEqual(events[2].title.value, "This is h1")

        self.assertEqual(events[3].date.dateFrom.realValue, "24.12.2020")
        self.assertEqual(events[3].date.dateTo.realValue, "24.12.2020")
        self.assertEqual(events[3].place.city, "Třebíč")
        self.assertEqual(events[3].priceRange, None)
        self.assertEqual(events[3].title.value, "This is h1")

        self.assertEqual(events[4].date.dateFrom.realValue, "26.12.2020")
        self.assertEqual(events[4].date.dateTo.realValue, "26.12.2020")
        self.assertEqual(events[4].place.city, "Mikulov")
        self.assertEqual(events[4].priceRange.priceFrom.text, "500 Kč")
        self.assertEqual(events[4].title.value, "This is title")

        self.assertEqual(events[5].date.dateFrom.realValue, "27.12.2020")
        self.assertEqual(events[5].date.dateTo.realValue, "27.12.2020")
        self.assertEqual(events[5].place.city, "Lednice")
        self.assertEqual(events[5].priceRange, None)
        self.assertEqual(events[5].title.value, "This is title")

        self.assertEqual(events[6].date.dateFrom.realValue, "29.12.2020")
        self.assertEqual(events[6].date.dateTo.realValue, "29.12.2020")
        self.assertEqual(events[6].place.city, "Hustopeče")
        self.assertEqual(events[6].priceRange, None)
        self.assertEqual(events[6].title.value, "This is title")

        self.assertEqual(events[7].date.dateFrom.realValue, "30.12.2020")
        self.assertEqual(events[7].date.dateTo.realValue, "31.12.2020")
        self.assertEqual(events[7].place.city, "Znojmo")
        self.assertEqual(events[7].priceRange.priceFrom.text, "300 Kč")
        self.assertEqual(events[7].priceRange.priceTo.text, "300 Kč")
        self.assertEqual(events[7].title.value, "This is parent h1")

        self.assertEqual(len(events), 8)
