import csv
import sys
import subprocess
import io
import os
from pathlib import Path
from dateutil import parser
import dateparser
import pickle

from src.EventParser import EventParser

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

verbose = 3

path = './data/test/'

total_results = []
total_events = 0
total_events_under_score_limit = 0

for filename in os.listdir(path):

    if not filename.startswith("29 "):
        continue

    if not filename.endswith(".html"):
        continue

    if verbose > 0:
        print("TESTING " + filename)

    html = open(path + filename, 'r', errors='ignore', encoding="utf-8").read()

    parsed_events = EventParser.parse(html)

    result_filename = new_filename = Path(filename).stem + ".txt"
    if verbose > 1:
        print("Found results")

        for parsed_event in parsed_events:
            print([parsed_event.title.value, parsed_event.date.dateFrom.realValue, parsed_event.date.dateTo.realValue,
                   parsed_event.place.city, "score: " + str(parsed_event.score)])
    # print(result_filename)

    expected_results = []

    with open(path + result_filename, newline='', encoding='utf-8', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|', )
        for row in spamreader:
            expected_results.append([*row])  # unwrap the results

    if verbose > 1:
        print("Expected results")
        for expected_result in expected_results:
            print(expected_result)

    # parsed_events.sort()
    expected_results.sort()

    results = []
    found_counter = 0

    expected_results_count = len(expected_results)

    for found in parsed_events:
        total_events += 1
        if found.score < 50:
            total_events_under_score_limit += 1

        found_title = found.title.value.lower().strip()
        found_alternative_title = found.title.alternative_value.lower().strip()
        if found_alternative_title == "":
            found_alternative_title = found_title

        found_date = found.date
        found_time = ""
        found_location = found.place.city.lower().strip()

        found_date_value = '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(
            found_date.dateFrom.datetime.month) + ". "
        found_date_value2 = found_date_value
        if found_date.dateFrom.datetime != found_date.dateTo.datetime:
            found_date_value = (
                    '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + '{:02d}'.format(
                found_date.dateFrom.datetime.month) + ". - " +
                    '{:02d}'.format(found_date.dateTo.datetime.day) + ". " + '{:02d}'.format(
                found_date.dateTo.datetime.month) + ". "
            )

            found_date_value2 = (
                    '{:02d}'.format(found_date.dateFrom.datetime.day) + ". " + "- " +
                    '{:02d}'.format(found_date.dateTo.datetime.day) + ". " + '{:02d}'.format(
                found_date.dateTo.datetime.month) + ". "
            )

        # found_price = found[4]

        for expected in expected_results:
            expected_title = expected[0].lower().strip()

            # temp - remove this when we support date ranges
            expected_date = expected[1].strip()
            # expected_date = expected_date.split("-")[-1]
            # expected_date = "".join(expected_date.split())  # remove all whitespaces in date

            expected_time = expected[2]
            expected_location = expected[3].lower().strip()
            # expected_price = expected[4]

            # expected_date_failed = False
            # expected_date_parsed = None
            # expected_date_parsed2 = None
            # try:
            #     expected_date_parsed = parser.parse(expected_date)
            # except ValueError:
            #     expected_date_parsed = None
            #
            # try:
            #     expected_date_parsed2 = dateparser.parse(expected_date, languages=["cs"])
            # except ValueError:
            #     expected_date_parsed2 = None
            #     pass
            #
            # if expected_date_parsed is None and expected_date_parsed2 is None:
            #     expected_results_count -= 1  # e.g. when date in results does not contain year, it is not recognized
            #     expected_results.remove(expected)

            if verbose > 2:
                print("test\n")
                print(found_title + " / " + expected_title + " = " + repr(found_title in expected_title))
                print(found_location + " / " + expected_location + " = " + repr(found_location in expected_location))
                # print(found_date.realValue + " / " + expected_date + " = " + repr(found_date.realValue == expected_date))
                # print(repr(found_date.datetime) + " / " + repr(expected_date_parsed) + " = " + repr(found_date.datetime == expected_date_parsed))
                # print(repr(found_date.datetime) + " / " + repr(expected_date_parsed2) + " = " + repr(found_date.datetime == expected_date_parsed2))
                print(repr(found_date.dateFrom.datetime) + " / " + repr(expected_date) + " = " + repr(
                    found_date.dateFrom.realValue == expected_date))
                print(repr(found_date.dateTo.datetime) + " / " + repr(expected_date) + " = " + repr(
                    found_date.dateTo.realValue == expected_date))
                print(repr(found_date_value) + " / " + repr(expected_date) + " = " + repr(
                    found_date_value in expected_date))
                print(repr(found_date_value2) + " / " + repr(expected_date) + " = " + repr(
                    found_date_value2 in expected_date))
                print("test\n")

            if (
                    (found_title in expected_title or expected_title in found_title
                     or found_alternative_title in expected_title or expected_title in found_alternative_title
                    )
                    and found_location in expected_location
                    and (
                    found_date is not None and found_date_value in expected_date or
                    found_date is not None and found_date_value2 in expected_date
            ) and found.score > 50
            ):
                print("FOUND MATCH: ")
                print("Name: " + found_title + ", date: " + found_date_value + ", place: " + found_location)

                found_counter += 1
                expected_results.remove(expected)
                break

    total_results.append([filename, found_counter, expected_results_count])

    print("NOT FOUND")
    for expected_result in expected_results:
        print(expected_result)

print("PREVIOUS TOTAL RESULTS")
try:
    with open('outfile', 'rb') as fp:
        itemlist = pickle.load(fp)
        for item in itemlist:
            print('\t'.join(map(str, item)))
except FileNotFoundError:
    pass

print("\n")
print("TOTAL RESULTS")
total_found = 0
total_expected = 0
for result in total_results:
    total_found += result[1]
    total_expected += result[2]
    print('\t'.join(map(str, result)))

with open('outfile', 'wb') as fp:
    pickle.dump(total_results, fp)

print("TOTAL PERCENTAGE: " + repr(total_found) + "/" + repr(total_expected) + " = " + repr(
    round(total_found / total_expected * 100, 2)) + "%")

print("TOTAL (included fake positive) found " + str(total_events))
print("TOTAL under limit found" + str(total_events_under_score_limit))