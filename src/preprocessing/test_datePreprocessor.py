from unittest import TestCase
from bs4 import BeautifulSoup

from src.preprocessing.DatePreprocessor import DatePreprocessor


class TestDatePreprocessor(TestCase):
    def test_find_single_title_h1(self):
        html = "<html>" \
               "<body>" \
               "<div><div>" \
               "<li><div>Led</div><div>1</div></li>" \
               "<li><div>úno</div><div>3</div></li>" \
               "<li><div>bře</div><div>5</div></li>" \
               "<li><div>dub</div><div>7</div></li>" \
               "<li><div>KVĚ</div><div>9</div></li>" \
               "<li><div>ČVN</div><div>11</div></li>" \
               "<li><div>ČVC</div><div>13</div></li>" \
               "<li><div>SRP</div><div>15</div></li>" \
               "<li><div>SEP</div><div>17</div></li>" \
               "<li><div>Oct</div><div>19</div></li>" \
               "<li><div>Lis</div><div>21</div></li>" \
               "<li><div>pro</div><div>23</div></li>" \
               "<li><div>Led.</div><div>1</div></li>" \
               "<li><div>úno.</div><div>3</div></li>" \
               "<li><div>bře.</div><div>5</div></li>" \
               "<li><div>dub.</div><div>7</div></li>" \
               "<li><div>KVĚ.</div><div>9</div></li>" \
               "<li><div>ČVN.</div><div>11</div></li>" \
               "<li><div>ČVC.</div><div>13</div></li>" \
               "<li><div>SRP.</div><div>15</div></li>" \
               "<li><div>SEP.</div><div>17</div></li>" \
               "<li><div>Oct.</div><div>19</div></li>" \
               "<li><div>Lis.</div><div>21</div></li>" \
               "<li><div>pro.</div><div>23</div></li>" \
               "<li><div>Led.</div><div>1</div><div>2021</div></li>" \
               "<li><div>úno.</div><div>3</div><div>2021</div></li>" \
               "<li><div>bře.</div><div>5</div><div>2021</div></li>" \
               "<li><div>dub.</div><div>7</div><div>2021</div></li>" \
               "<li><div>KVĚ.</div><div>9</div><div>2021</div></li>" \
               "<li><div>ČVN.</div><div>11</div><div>2021</div></li>" \
               "<li><div>ČVC.</div><div>13</div><div>2021</div></li>" \
               "<li><div>SRP.</div><div>15</div><div>2021</div></li>" \
               "<li><div>SEP.</div><div>17</div><div>2021</div></li>" \
               "<li><div>Oct.</div><div>19</div><div>2021</div></li>" \
               "<li><div>Lis.</div><div>21</div><div>2021</div></li>" \
               "<li><div>pro.</div><div>23</div><div>2021</div></li>" \
               "</div></div>" \
               "</body>" \
               "</html>"
        soup = BeautifulSoup(html, 'html.parser')

        soup = DatePreprocessor.fix_dates(soup)

        dates = soup.find_all("li")
        print(repr(dates))
        self.assertNotEqual(dates[0].find(text="1 Led 2020"), None)
        self.assertNotEqual(dates[1].find(text="3 úno 2020"), None)
        self.assertNotEqual(dates[2].find(text="5 bře 2020"), None)
        self.assertNotEqual(dates[3].find(text="7 dub 2020"), None)
        self.assertNotEqual(dates[4].find(text="9 KVĚ 2020"), None)
        self.assertNotEqual(dates[5].find(text="11 ČVN 2020"), None)
        self.assertNotEqual(dates[6].find(text="13 ČVC 2020"), None)
        self.assertNotEqual(dates[7].find(text="15 SRP 2020"), None)
        self.assertNotEqual(dates[8].find(text="17 SEP 2020"), None)
        self.assertNotEqual(dates[9].find(text="19 Oct 2020"), None)
        self.assertNotEqual(dates[10].find(text="21 Lis 2020"), None)
        self.assertNotEqual(dates[11].find(text="23 pro 2020"), None)

        self.assertNotEqual(dates[12].find(text="1 Led 2020"), None)
        self.assertNotEqual(dates[13].find(text="3 úno 2020"), None)
        self.assertNotEqual(dates[14].find(text="5 bře 2020"), None)
        self.assertNotEqual(dates[15].find(text="7 dub 2020"), None)
        self.assertNotEqual(dates[16].find(text="9 KVĚ 2020"), None)
        self.assertNotEqual(dates[17].find(text="11 ČVN 2020"), None)
        self.assertNotEqual(dates[18].find(text="13 ČVC 2020"), None)
        self.assertNotEqual(dates[19].find(text="15 SRP 2020"), None)
        self.assertNotEqual(dates[20].find(text="17 SEP 2020"), None)
        self.assertNotEqual(dates[21].find(text="19 Oct 2020"), None)
        self.assertNotEqual(dates[22].find(text="21 Lis 2020"), None)
        self.assertNotEqual(dates[23].find(text="23 pro 2020"), None)

        self.assertNotEqual(dates[24].find(text="1 Led 2021"), None)
        self.assertNotEqual(dates[25].find(text="3 úno 2021"), None)
        self.assertNotEqual(dates[26].find(text="5 bře 2021"), None)
        self.assertNotEqual(dates[27].find(text="7 dub 2021"), None)
        self.assertNotEqual(dates[28].find(text="9 KVĚ 2021"), None)
        self.assertNotEqual(dates[29].find(text="11 ČVN 2021"), None)
        self.assertNotEqual(dates[30].find(text="13 ČVC 2021"), None)
        self.assertNotEqual(dates[31].find(text="15 SRP 2021"), None)
        self.assertNotEqual(dates[32].find(text="17 SEP 2021"), None)
        self.assertNotEqual(dates[33].find(text="19 Oct 2021"), None)
        self.assertNotEqual(dates[34].find(text="21 Lis 2021"), None)
        self.assertNotEqual(dates[35].find(text="23 pro 2021"), None)

