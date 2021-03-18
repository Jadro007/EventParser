from unittest import TestCase

from bs4 import BeautifulSoup
from src.finder.PriceFinder import PriceFinder
from src.finder.TimeFinder import TimeFinder


class TestTimeFinder(TestCase):
    def test_find_no_time(self):
        html = "<html><body><div>" \
               "<li></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TimeFinder.find(soup)

        self.assertEqual(results, None)

    def test_find_single_price(self):
        html = "<html><body><div>" \
               "<li>17:00</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TimeFinder.find(soup)

        self.assertEqual(results[0].value, "17:00")

    def test_find_single_price_different_format(self):
        html = "<html><body><div>" \
               "<li>17 hod</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TimeFinder.find(soup)

        self.assertEqual(results[0].value, "17:00")

    def test_find_multiple_time(self):
        html = "<html><body><div>" \
               "<li>12:00</li>" \
               "<li>17:00</li>" \
               "<li>20:00</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TimeFinder.find(soup)

        self.assertEqual(results[0].value, "12:00")
        self.assertEqual(results[1].value, "17:00")
        self.assertEqual(results[2].value, "20:00")

    def test_find_multiple_time_mixed_format(self):
        html = "<html><body><div>" \
               "<li>12 hod.</li>" \
               "<li>17:00</li>" \
               "<li>20:05</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TimeFinder.find(soup)

        self.assertEqual(results[0].value, "12:00")
        self.assertEqual(results[1].value, "17:00")
        self.assertEqual(results[2].value, "20:05")


    def test_find_multiple_price_in_one_element(self):
        html = "<html><body><div>" \
               "<li>17:00, 20:00 večer</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TimeFinder.find(soup)

        self.assertEqual(results[0].value, "17:00")
        self.assertEqual(results[1].value, "20:00")
