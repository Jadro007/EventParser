from unittest import TestCase
from bs4 import BeautifulSoup

from src.parser.SingleEventParser import SingleEventParser


class TestSingleEventParser(TestCase):
    def test_parse(self):

        html = "<html>" \
                   "<body>" \
                       "<div><h1>This is sparta</h1>21.12.2020, Jihlava, 100 Kč, 200 Kč</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        event = SingleEventParser.parse(soup)

        self.assertEqual(event.date.realValue, "21.12.2020")
        self.assertEqual(event.place.city, "Jihlava")
        self.assertEqual(event.priceRange.priceFrom.text, "100 Kč")
        self.assertEqual(event.priceRange.priceTo.text, "200 Kč")
        self.assertEqual(event.title.value, "This is sparta")

