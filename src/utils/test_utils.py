from unittest import TestCase
from bs4 import BeautifulSoup
from src.utils.Utils import Utils


class TestUtils(TestCase):
    def test_get_depth(self):

        html = "<html><body><div>" \
               "<li>Brno</li>" \
               "<li>Tohle je Jihlava, kousek po D1</li>" \
               "<li>Praha <span id=\"depth6\">u Brna</span></li>" \
               "<li id=\"depth5\">Třebíč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        self.assertEqual(Utils.get_depth(soup.find(id="depth5")), 5)
        self.assertEqual(Utils.get_depth(soup.find(id="depth6")), 6)


    def test_lowest_common_ancestor(self):

        html = "<html><body><div id=\"child7\">" \
               "<li>Brno</li>" \
               "<li>Tohle je Jihlava, kousek po D1</li>" \
               "<li id=\"child3\">Praha <span id=\"child2\">u Brna</span><span id=\"child1\">u Brna<span id=\"child6\">u Brna</span></span></li>" \
               "<li id=\"child4\">Třebíč</li>" \
               "</div></body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        self.assertEqual(Utils.lowest_common_ancestor(soup.find(id="child2"), soup.find(id="child2")), soup.find(id="child2"))
        self.assertEqual(Utils.lowest_common_ancestor(soup.find(id="child2"), soup.find(id="child6")), soup.find(id="child3"))
        self.assertEqual(Utils.lowest_common_ancestor(soup.find(id="child6"), soup.find(id="child1")), soup.find(id="child1"))
        self.assertEqual(Utils.lowest_common_ancestor(soup.find(id="child3"), soup.find(id="child4")), soup.find(id="child7"))
        self.assertEqual(Utils.lowest_common_ancestor(soup.find(id="child6"), soup.find(id="child4")), soup.find(id="child7"))
