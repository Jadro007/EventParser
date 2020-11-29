from unittest import TestCase
from bs4 import BeautifulSoup

from src.preprocessing.DatePreprocessor import DatePreprocessor
from src.preprocessing.RemovalPreprocessor import RemovalPreprocessor


class TestRemovalPreprocessor(TestCase):
    def test_unwrapping_elements(self):
        html = "<html>" \
                "<body>" \
                    "<li>" \
                        "<span>20</span>" \
                        "<span><small>Říj.</small> 2020</span>" \
                        "<span><b>19:30</b> baf</span>" \
                    "</li>" \
                "</body>" \
                "</html>"

        soup = BeautifulSoup(html, 'html.parser')

        soup = RemovalPreprocessor.unwrap(soup)

        elememt = soup.find("li")
        self.assertNotEqual(elememt.getText(), "20 Říj. 2020 19:30 baf")
