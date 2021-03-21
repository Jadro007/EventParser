from unittest import TestCase

from bs4 import BeautifulSoup
from src.finder.PriceFinder import PriceFinder


class TestPriceFinder(TestCase):
    def test_find_no_price(self):
        html = "<html><body><div>" \
               "<li></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results, None)

    def test_find_single_price(self):
        html = "<html><body><div>" \
               "<li>100 Kč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100 Kč")
        self.assertEqual(results.priceFrom.currency, "Kč")
        self.assertEqual(results.priceTo.value, 100)
        self.assertEqual(results.priceTo.text, "100 Kč")
        self.assertEqual(results.priceTo.currency, "Kč")

    def test_find_single_price_different_currency(self):
        html = "<html><body><div>" \
               "<li>100 ,-</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100 ,-")
        self.assertEqual(results.priceFrom.currency, ",-")
        self.assertEqual(results.priceTo.value, 100)
        self.assertEqual(results.priceTo.text, "100 ,-")
        self.assertEqual(results.priceTo.currency, ",-")

    def test_find_single_price_without_space(self):
        html = "<html><body><div>" \
               "<li>100kc</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100kc")
        self.assertEqual(results.priceFrom.currency, "kc")
        self.assertEqual(results.priceTo.value, 100)
        self.assertEqual(results.priceTo.text, "100kc")
        self.assertEqual(results.priceTo.currency, "kc")

    def test_find_single_price_inside_text(self):
        html = "<html><body><div>" \
               "<li>Tohle stoji 100 Kč ale stoji to za to</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100 Kč")
        self.assertEqual(results.priceFrom.currency, "Kč")
        self.assertEqual(results.priceTo.value, 100)
        self.assertEqual(results.priceTo.text, "100 Kč")
        self.assertEqual(results.priceTo.currency, "Kč")

    def test_find_multiple_price(self):
        html = "<html><body><div>" \
               "<li>100 Kč</li>" \
               "<li>200 Kč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100 Kč")
        self.assertEqual(results.priceFrom.currency, "Kč")
        self.assertEqual(results.priceTo.value, 200)
        self.assertEqual(results.priceTo.text, "200 Kč")
        self.assertEqual(results.priceTo.currency, "Kč")

    def test_find_multiple_price_in_one_element(self):
        html = "<html><body><div>" \
               "<li>100 Kč, 200 Kč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100 Kč")
        self.assertEqual(results.priceFrom.currency, "Kč")
        self.assertEqual(results.priceTo.value, 200)
        self.assertEqual(results.priceTo.text, "200 Kč")
        self.assertEqual(results.priceTo.currency, "Kč")

    def test_find_multiple_price_in_different_order(self):
        html = "<html><body><div>" \
               "<li>200 Kč</li>" \
               "<li>100 Kč</li>" \
               "<li>300 Kč</li>" \
               "<li>50 Kč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 50)
        self.assertEqual(results.priceFrom.text, "50 Kč")
        self.assertEqual(results.priceFrom.currency, "Kč")
        self.assertEqual(results.priceTo.value, 300)
        self.assertEqual(results.priceTo.text, "300 Kč")
        self.assertEqual(results.priceTo.currency, "Kč")

    def test_find_price_range(self):
        html = "<html><body><div>" \
               "<li>100-200 Kč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = PriceFinder.find(soup)

        self.assertEqual(results.priceFrom.value, 100)
        self.assertEqual(results.priceFrom.text, "100-200 Kč")
        self.assertEqual(results.priceFrom.currency, "Kč")
        self.assertEqual(results.priceTo.value, 200)
        self.assertEqual(results.priceTo.text, "100-200 Kč")
        self.assertEqual(results.priceTo.currency, "Kč")

