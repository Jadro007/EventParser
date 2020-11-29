from unittest import TestCase
from bs4 import BeautifulSoup

from src.enhancer.GroupEnhancer import GroupEnhancer
from src.finder.DateFinder import DateFinder
from src.finder.PlaceFinder import PlaceFinder
from src.utils.Utils import Utils


class TestGroupEnhancer(TestCase):
    def test_parse_groups_single_list(self):
        html = "<html>" \
                   "<body>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)


        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))

    def test_parse_groups_two_lists_same_depth(self):
        html = "<html>" \
                   "<body>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                       "<div id=\"group2\">" \
                           "<li>21.3.2020, Jihlava</li>" \
                           "<li>22.3.2020, Brno</li>" \
                           "<li>23.3.2020, Praha</li>" \
                           "<li>24.3.2020, Třebíč</li>" \
                       "</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)


        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))


        self.assertEqual(dates[4].group.container, soup.find(id="group2"))
        self.assertEqual(dates[5].group.container, soup.find(id="group2"))
        self.assertEqual(dates[6].group.container, soup.find(id="group2"))
        self.assertEqual(dates[7].group.container, soup.find(id="group2"))

    def test_parse_groups_empty(self):
        html = "<html>" \
                   "<body>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)


        self.assertEqual(dates, [])

    def test_parse_groups_single_item(self):
        html = "<html>" \
                   "<body id=\"group1\">" \
                       "<div>21.12.2020, Jihlava</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(None, dates[0].group)

    def test_parse_groups_two_lists_different_depth(self):
        html = "<html>" \
                   "<body>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                       "<div>" \
                            "<div id=\"group2\">" \
                               "<li>21.3.2020, Jihlava</li>" \
                               "<li>22.3.2020, Brno</li>" \
                               "<li>23.3.2020, Praha</li>" \
                               "<li>24.3.2020m Třebíč</li>" \
                            "</div>" \
                       "</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))

        self.assertEqual(dates[4].group.container, soup.find(id="group2"))
        self.assertEqual(dates[5].group.container, soup.find(id="group2"))
        self.assertEqual(dates[6].group.container, soup.find(id="group2"))
        self.assertEqual(dates[7].group.container, soup.find(id="group2"))

    def test_parse_groups_two_lists_different_depth_and_one_single_event(self):
        html = "<html>" \
               "<body>" \
                       "<div>" \
                            "20.12.2020, Jihlava" \
                       "</div>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                       "<div>" \
                            "<div id=\"group2\">" \
                               "<li>21.3.2020, Jihlava</li>" \
                               "<li>22.3.2020, Brno</li>" \
                               "<li>23.3.2020, Praha</li>" \
                               "<li>24.3.2020, Třebíč</li>" \
                            "</div>" \
                       "</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group, None)
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))
        self.assertEqual(dates[4].group.container, soup.find(id="group1"))

        self.assertEqual(dates[5].group.container, soup.find(id="group2"))
        self.assertEqual(dates[6].group.container, soup.find(id="group2"))
        self.assertEqual(dates[7].group.container, soup.find(id="group2"))
        self.assertEqual(dates[8].group.container, soup.find(id="group2"))

    def test_parse_groups_single_list_and_one_single_event(self):
        html = "<html>" \
               "<body><div id=\"group1\">" \
               "<li>21.12.2020, Jihlava</li>" \
               "<li>22.12.2020, Brno</li>" \
               "<li>23.12.2020, Praha</li>" \
               "<li>24.12.2020, Třebíč</li>" \
               "</div>" \
               "<div>31.12.2020, Znojmo</div>" \
               "</body>" \
               "</html>"

        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))
        # self.assertEqual(dates[4].group, None)

    def test_parse_groups_two_lists_different_depth_really_deep(self):
        html = "<html>" \
                   "<body>" \
                       "<div><div><div><div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div></div></div>" \
                       "<div>" \
                            "<div><div><div><div><div><div id=\"group2\">" \
                               "<li>21.3.2020, Jihlava</li>" \
                               "<li>22.3.2020, Brno</li>" \
                               "<li>23.3.2020, Praha</li>" \
                               "<li>24.3.2020m Třebíč</li>" \
                            "</div></div></div></div></div></div>" \
                       "</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))

        self.assertEqual(dates[4].group.container, soup.find(id="group2"))
        self.assertEqual(dates[5].group.container, soup.find(id="group2"))
        self.assertEqual(dates[6].group.container, soup.find(id="group2"))
        self.assertEqual(dates[7].group.container, soup.find(id="group2"))


    def test_parse_groups_nested_lists(self):
        html = "<html>" \
                   "<body>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno" \
                               "<div id=\"group2\">" \
                               "<li>21.3.2020, Jihlava</li>" \
                               "<li>22.3.2020, Brno</li>" \
                               "<li>23.3.2020, Praha</li>" \
                               "<li>24.3.2020, Třebíč</li>" \
                               "</div>" \
                           "</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020. Třebíč</li>" \
                       "</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)


        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))

        self.assertEqual(dates[2].group.container, soup.find(id="group2"))
        self.assertEqual(dates[3].group.container, soup.find(id="group2"))
        self.assertEqual(dates[4].group.container, soup.find(id="group2"))
        self.assertEqual(dates[5].group.container, soup.find(id="group2"))

        self.assertEqual(dates[6].group.container, soup.find(id="group1"))
        self.assertEqual(dates[7].group.container, soup.find(id="group1"))

    def test_parse_groups_two_lists_different_depth_really_deep(self):
        html = "<html>" \
                   "<body>" \
                       "<div><div><div><div id=\"group1\">" \
                           "<li>21.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div></div></div></div>" \
                       "<div>" \
                            "<div><div><div><div><div><div id=\"group2\">" \
                               "<li>21.3.2020, Jihlava</li>" \
                               "<li>22.3.2020, Brno</li>" \
                               "<li>23.3.2020, Praha</li>" \
                               "<li>24.3.2020, Třebíč</li>" \
                            "</div></div></div></div></div></div>" \
                       "</div>" \
                   "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))

        self.assertEqual(dates[4].group.container, soup.find(id="group2"))
        self.assertEqual(dates[5].group.container, soup.find(id="group2"))
        self.assertEqual(dates[6].group.container, soup.find(id="group2"))
        self.assertEqual(dates[7].group.container, soup.find(id="group2"))

        def test_parse_groups_two_lists_same_depth(self):
            html = "<html>" \
                   "<body>" \
                   "<div id=\"group1\">" \
                   "<li>21.12.2020, Jihlava</li>" \
                   "<li>22.12.2020, Brno</li>" \
                   "<li>23.12.2020, Praha</li>" \
                   "<li>24.12.2020, Třebíč</li>" \
                   "</div>" \
                   "<div id=\"group2\">" \
                   "<li>21.3.2020, Jihlava</li>" \
                   "<li>22.3.2020, Brno</li>" \
                   "<li>23.3.2020, Praha</li>" \
                   "<li>24.3.2020, Třebíč</li>" \
                   "</div>" \
                   "</body>" \
                   "</html>"
            soup = BeautifulSoup(html, 'html.parser')

            dates = DateFinder.find(soup)

            GroupEnhancer.set_groups(dates)

            self.assertEqual(dates[0].group.container, soup.find(id="group1"))
            self.assertEqual(dates[1].group.container, soup.find(id="group1"))
            self.assertEqual(dates[2].group.container, soup.find(id="group1"))
            self.assertEqual(dates[3].group.container, soup.find(id="group1"))

            self.assertEqual(dates[4].group.container, soup.find(id="group2"))
            self.assertEqual(dates[5].group.container, soup.find(id="group2"))
            self.assertEqual(dates[6].group.container, soup.find(id="group2"))
            self.assertEqual(dates[7].group.container, soup.find(id="group2"))

    def test_parse_groups_single_list_multiple_dates_per_element(self):
        html = "<html>" \
                   "<body>" \
                       "<div id=\"group1\">" \
                           "<li>21.12.2020 - 31.12.2020, Jihlava</li>" \
                           "<li>22.12.2020, Brno</li>" \
                           "<li>23.12.2020, Praha</li>" \
                           "<li>24.12.2020, Třebíč</li>" \
                       "</div>" \
                    "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))
        self.assertEqual(dates[4].group.container, soup.find(id="group1"))

    def test_parse_groups_single_list_multiple_dates_per_element_mixed_with_single_dates(self):
        html = "<html>" \
               "<body>" \
               "<div id=\"group1\">" \
                   "<div>" \
                        "<div>14.11.2020</div>" \
                    "</div>" \
                    "<div>" \
                     "<div>16.10.2020 18.10.2020</div>" \
                    "</div>" \
                    "<div>" \
                        "<div>8.7.2020 11.7.2020</div>" \
                    "</div>" \
                    "<div>" \
                        "<div>28.11.2020</div>" \
                    "</div>" \
               "</div>" \
               "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        dates = DateFinder.find(soup)

        GroupEnhancer.set_groups(dates)

        self.assertEqual(dates[0].group.container, soup.find(id="group1"))
        self.assertEqual(dates[1].group.container, soup.find(id="group1"))
        self.assertEqual(dates[2].group.container, soup.find(id="group1"))
        self.assertEqual(dates[3].group.container, soup.find(id="group1"))
        self.assertEqual(dates[4].group.container, soup.find(id="group1"))
        self.assertEqual(dates[5].group.container, soup.find(id="group1"))
