from unittest import TestCase

from bs4 import BeautifulSoup
from src.finder.PriceFinder import PriceFinder
from src.finder.TitleFinder import TitleFinder


class TestTitleFinder(TestCase):
    def test_list_events_find_no_price(self):
        html = "<html><body><div>" \
               "<li></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup)

        self.assertEqual(results, None)

    def test_list_events_find_single_title_h1(self):
        html = "<html><body><div>" \
               "<li><h1>This is sparta</h1></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup)

        self.assertEqual(results.value, "This is sparta")


    def test_list_events_find_single_title_h2(self):
        html = "<html><body><div>" \
               "<li><h2>This is sparta</h2></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup)

        self.assertEqual(results.value, "This is sparta")

    def test_list_events_find_single_title_h3(self):
        html = "<html><body><div>" \
               "<li><h3>This is sparta</h3></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup)

        self.assertEqual(results.value, "This is sparta")

    def test_list_events_find_single_title_h4(self):
        html = "<html><body><div>" \
               "<li><h4>This is Patrick</h4></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup)

        self.assertEqual(results.value, "This is Patrick")

    def test_list_events_find_single_title_in_title(self):
        html = "<html><title>This is title</title><body><div>" \
               "<li>This is nothing</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup)

        self.assertEqual(results.value, "This is title")

    def test_list_events_find_title_in_parents(self):
        html = "<html><body><h1>This is sparta</h1><div>" \
               "<li>nothing here</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup.find("li"))

        self.assertEqual(results.value, "This is sparta")
        self.assertEqual(results.container, soup.find("h1"))


    def test_list_events_find_with_selected_event_outside_of_other_events_takes_h1(self):
        # this is here to test that it will not take titles from other events
        html = "<html>" \
                   "<h1>This is title</h1>" \
                   "<body>" \
                       "<div><h1>This is parent h1</h1><div id=\"group1\">" \
                           "<li><h1>This is h1</h1>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li><h2>This is h2</h2>22.12.2020, Brno, 200 Kč</li>" \
                           "<li><h3>This is h3</h3>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div>" \
                       "<h1 id=\"znojmo_title\">This is title</h1><div id=\"znojmo\">31.12.2020, Znojmo, 300 Kč</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup.find(id="znojmo"))

        self.assertEqual(results.value, "This is title")
        self.assertEqual(results.container, soup.find(id="znojmo_title"))

    def test_list_events_find_with_selected_event_outside_of_other_events_takes_title_in_head(self):
        # this is here to test that it will not take titles from other events
        html = "<html>" \
                   "<head><title>This is title</title></head>" \
                   "<body>" \
                       "<div><h1>This is parent h1</h1><div id=\"group1\">" \
                           "<li><h1>This is h1</h1>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li><h2>This is h2</h2>22.12.2020, Brno, 200 Kč</li>" \
                           "<li><h3>This is h3</h3>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div>" \
                       "<div id=\"znojmo\">31.12.2020, Znojmo, 300 Kč</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup.find(id="znojmo"))

        self.assertEqual(results.value, "This is title")
        self.assertEqual(results.container, soup.find("title"))

    def test_single_event_find_no_price(self):
        html = "<html><body><div>" \
               "<li></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup, True)

        self.assertEqual(results, None)

    def test_single_event_find_single_title_h1(self):
        html = "<html><body><div>" \
               "<li><h1>This is sparta</h1></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup, True)

        self.assertEqual(results.value, "This is sparta")


    def test_single_event_find_single_title_h2(self):
        html = "<html><body><div>" \
               "<li><h2>This is sparta</h2></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup, True)

        self.assertEqual(results.value, "This is sparta")

    def test_single_event_find_single_title_h3(self):
        html = "<html><body><div>" \
               "<li><h3>This is sparta</h3></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup, True)

        self.assertEqual(results.value, "This is sparta")

    def test_single_event_find_single_title_h4(self):
        html = "<html><body><div>" \
               "<li><h4>This is Patrick</h4></li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup, True)

        self.assertEqual(results.value, "This is Patrick")

    def test_single_event_find_single_title_in_title(self):
        html = "<html><title>This is title</title><body><div>" \
               "<li>This is nothing</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup, True)

        self.assertEqual(results.value, "This is title")

    def test_single_event_find_title_in_parents(self):
        html = "<html><body><h1>This is sparta</h1><div>" \
               "<li>nothing here</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup.find("li"), True)

        self.assertEqual(results.value, "This is sparta")
        self.assertEqual(results.container, soup.find("h1"))


    def test_single_event_find_takes_correct_title(self):
        # this is here to test that it will take titles
        html = "<html>" \
                   "<h1 id=\"mainTitle\">This is main title</h1>" \
                   "<body>" \
                       "<div><h1>This is parent h1</h1><div id=\"group1\">" \
                           "<li><h1>This is h1</h1>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li><h2>This is h2</h2>22.12.2020, Brno, 200 Kč</li>" \
                           "<li><h3>This is h3</h3>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div>" \
                       "<h1 id=\"znojmo_title\">This is title</h1><div id=\"znojmo\">31.12.2020, Znojmo, 300 Kč</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup.find(id="znojmo"), True)

        self.assertEqual(results.value, "This is main title")
        self.assertEqual(results.container, soup.find(id="mainTitle"))

    def test_single_event_find_takes_correct_title_test2(self):
        # this is here to test that it will not take titles from other events
        html = "<html>" \
                   "<head><title>This is title</title></head>" \
                   "<body>" \
                       "<div><h1>This is parent h1</h1><div id=\"group1\">" \
                           "<li><h1>This is h1</h1>21.12.2020, Jihlava, 100 Kč, 130 Kč</li>" \
                           "<li><h2>This is h2</h2>22.12.2020, Brno, 200 Kč</li>" \
                           "<li><h3>This is h3</h3>23.12.2020, Praha, 150 Kč</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div>" \
                       "<div id=\"znojmo\">31.12.2020, Znojmo, 300 Kč</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = TitleFinder.find(soup.find(id="znojmo"), True)

        self.assertEqual(results.value, "This is parent h1")
        self.assertEqual(results.container, soup.find("h1"))