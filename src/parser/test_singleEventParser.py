from unittest import TestCase
from bs4 import BeautifulSoup

from src.parser.SingleEventParser import SingleEventParser


class TestSingleEventParser(TestCase):
    def test_parse(self):

        html = "<html>" \
                   "<body>" \
                       "<div>21.12.2020, Jihlava</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        event = SingleEventParser.parse(soup)

        self.assertEqual(event.date.realValue, "21.12.2020")
        self.assertEqual(event.place.city, "Jihlava")

