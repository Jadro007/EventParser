import datetime
from unittest import TestCase

from bs4 import BeautifulSoup

from src.dto.Date import Date
from src.finder.DateFinder import DateFinder


class TestDateFinder(TestCase):
    def test_find(self):


        html = "<html><body>" \
               "<li>10.12.2020</li>" \
               "<li>10.4.2020</li>" \
               "<li>1.5.2020</li>" \
               "<li>1.11.2020</li>" \
               "<li>3.4.2020</li>" \
               "<li>2.2.2020</li>" \
               "<li>10/12/2020</li>" \
               "<li>10/4/2020</li>" \
               "<li>1/5/2020</li>" \
               "<li>1/11/2020</li>" \
               "<li>3/4/2020</li>" \
               "<li>2/2/2020</li>" \
               "<li>10-12-2020</li>" \
               "<li>10-4-2020</li>" \
               "<li>1-5-2020</li>" \
               "<li>1-11-2020</li>" \
               "<li>3-4-2020</li>" \
               "<li>2-2-2020</li>" \
               "<li>10 12 2020</li>" \
               "<li>10 4 2020</li>" \
               "<li>1 5 2020</li>" \
               "<li>1 11 2020</li>" \
               "<li>3 4 2020</li>" \
               "<li>2 2 2020</li>" \
               "<li>10.12. 2020</li>" \
               "<li>10-4. 2020</li>" \
               "<li>1/5 2020</li>" \
               "<li>1. 11. 2020</li>" \
               "<li>3. 4. 2020</li>" \
               "<li>2. 2. 2020</li>" \
               "<li>10. prosinec 2020</li>" \
               "<li>10.dubna 2020</li>" \
               "<li>1. května 2020</li>" \
               "<li>1. listopad 2020</li>" \
               "<li>3. duben 2020</li>" \
               "<li>2. února 2020</li>" \
               "<li>5. 12.</li>" \
               "<li>7. března</li>" \
               "</body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        results = DateFinder.find(soup)

        # . separator
        self.assertEqual(results[0].realValue, "10.12.2020")
        self.assertEqual(results[0].datetime, datetime.datetime(2020, 12, 10))

        self.assertEqual(results[1].realValue, "10.4.2020")
        self.assertEqual(results[1].datetime, datetime.datetime(2020, 4, 10))

        self.assertEqual(results[2].realValue, "1.5.2020")
        self.assertEqual(results[2].datetime, datetime.datetime(2020, 5, 1))

        self.assertEqual(results[3].realValue, "1.11.2020")
        self.assertEqual(results[3].datetime, datetime.datetime(2020, 11, 1))

        self.assertEqual(results[4].realValue, "3.4.2020")
        self.assertEqual(results[4].datetime, datetime.datetime(2020, 4, 3))

        self.assertEqual(results[5].realValue, "2.2.2020")
        self.assertEqual(results[5].datetime, datetime.datetime(2020, 2, 2))

        # / separator
        self.assertEqual(results[6].realValue, "10/12/2020")
        self.assertEqual(results[6].datetime, datetime.datetime(2020, 12, 10))

        self.assertEqual(results[7].realValue, "10/4/2020")
        self.assertEqual(results[7].datetime, datetime.datetime(2020, 4, 10))

        self.assertEqual(results[8].realValue, "1/5/2020")
        self.assertEqual(results[8].datetime, datetime.datetime(2020, 5, 1))

        self.assertEqual(results[9].realValue, "1/11/2020")
        self.assertEqual(results[9].datetime, datetime.datetime(2020, 11, 1))

        self.assertEqual(results[10].realValue, "3/4/2020")
        self.assertEqual(results[10].datetime, datetime.datetime(2020, 4, 3))

        self.assertEqual(results[11].realValue, "2/2/2020")
        self.assertEqual(results[11].datetime, datetime.datetime(2020, 2, 2))

        # - separator
        self.assertEqual(results[12].realValue, "10-12-2020")
        self.assertEqual(results[12].datetime, datetime.datetime(2020, 12, 10))

        self.assertEqual(results[13].realValue, "10-4-2020")
        self.assertEqual(results[13].datetime, datetime.datetime(2020, 4, 10))

        self.assertEqual(results[14].realValue, "1-5-2020")
        self.assertEqual(results[14].datetime, datetime.datetime(2020, 5, 1))

        self.assertEqual(results[15].realValue, "1-11-2020")
        self.assertEqual(results[15].datetime, datetime.datetime(2020, 11, 1))

        self.assertEqual(results[16].realValue, "3-4-2020")
        self.assertEqual(results[16].datetime, datetime.datetime(2020, 4, 3))

        self.assertEqual(results[17].realValue, "2-2-2020")
        self.assertEqual(results[17].datetime, datetime.datetime(2020, 2, 2))

        # (space) separator
        self.assertEqual(results[18].realValue, "10 12 2020")
        self.assertEqual(results[18].datetime, datetime.datetime(2020, 12, 10))

        self.assertEqual(results[19].realValue, "10 4 2020")
        self.assertEqual(results[19].datetime, datetime.datetime(2020, 4, 10))

        self.assertEqual(results[20].realValue, "1 5 2020")
        self.assertEqual(results[20].datetime, datetime.datetime(2020, 5, 1))

        self.assertEqual(results[21].realValue, "1 11 2020")
        self.assertEqual(results[21].datetime, datetime.datetime(2020, 11, 1))

        self.assertEqual(results[22].realValue, "3 4 2020")
        self.assertEqual(results[22].datetime, datetime.datetime(2020, 4, 3))

        self.assertEqual(results[23].realValue, "2 2 2020")
        self.assertEqual(results[23].datetime, datetime.datetime(2020, 2, 2))

        # mixed separator
        self.assertEqual(results[24].realValue, "10.12. 2020")
        self.assertEqual(results[24].datetime, datetime.datetime(2020, 12, 10))

        self.assertEqual(results[25].realValue, "10-4. 2020")
        self.assertEqual(results[25].datetime, datetime.datetime(2020, 4, 10))

        self.assertEqual(results[26].realValue, "1/5 2020")
        self.assertEqual(results[26].datetime, datetime.datetime(2020, 5, 1))

        self.assertEqual(results[27].realValue, "1. 11. 2020")
        self.assertEqual(results[27].datetime, datetime.datetime(2020, 11, 1))

        self.assertEqual(results[28].realValue, "3. 4. 2020")
        self.assertEqual(results[28].datetime, datetime.datetime(2020, 4, 3))

        self.assertEqual(results[29].realValue, "2. 2. 2020")
        self.assertEqual(results[29].datetime, datetime.datetime(2020, 2, 2))

        # named months
        self.assertEqual(results[30].realValue, "10. prosinec 2020")
        self.assertEqual(results[30].datetime, datetime.datetime(2020, 12, 10))

        self.assertEqual(results[31].realValue, "10.dubna 2020")
        self.assertEqual(results[31].datetime, datetime.datetime(2020, 4, 10))

        self.assertEqual(results[32].realValue, "1. května 2020")
        self.assertEqual(results[32].datetime, datetime.datetime(2020, 5, 1))

        self.assertEqual(results[33].realValue, "1. listopad 2020")
        self.assertEqual(results[33].datetime, datetime.datetime(2020, 11, 1))

        self.assertEqual(results[34].realValue, "3. duben 2020")
        self.assertEqual(results[34].datetime, datetime.datetime(2020, 4, 3))

        self.assertEqual(results[35].realValue, "2. února 2020")
        self.assertEqual(results[35].datetime, datetime.datetime(2020, 2, 2))

        # without a year
        self.assertEqual(results[36].realValue, "5. 12.")
        self.assertEqual(results[36].datetime, datetime.datetime(2021, 12, 5))

        self.assertEqual(results[37].realValue, "7. března")
        self.assertEqual(results[37].datetime, datetime.datetime(2021, 3, 7))
