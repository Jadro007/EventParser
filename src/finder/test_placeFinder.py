from unittest import TestCase

from bs4 import BeautifulSoup
from src.finder.PlaceFinder import PlaceFinder


class TestPlaceFinder(TestCase):
    def test_find(self):


        html = "<html><body><div>" \
               "<li>Brno</li>" \
               "<li>Tohle je Jihlava, kousek po D1</li>" \
               "<li>Praha</li>" \
               "<li>Třebíč</li>" \
               "<li>Bílov</li>" \
               "<li>Bílovec</li>" \
               "<li>Bor</li>" \
               "<li>borovička je super</li>" \
               "<li>Uherské Hradiště</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PlaceFinder.find(soup)

        self.assertEqual(results[0].city, "Brno")
        self.assertEqual(results[1].city, "Jihlava")
        self.assertEqual(results[2].city, "Praha")
        self.assertEqual(results[3].city, "Třebíč")
        self.assertEqual(results[4].city, "Bílov")
        self.assertEqual(results[5].city, "Bílovec")
        self.assertEqual(results[6].city, "Bor")
        self.assertEqual(results[7].city, "Uherské Hradiště")
