import io
import sys
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

cities = []
with open("./cities.csv", encoding="utf-8") as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        cities.append(row[1])


cities = [x.strip() for x in cities]

result = []

print ("started", flush=True)
i = 0

cities = list(set(cities))
cities.sort()

with open("cities_list.txt", "a", encoding="utf-8") as f:
    for city in cities:

        print(city + " is valid \n", flush=True)
        f.write(city + "\n")





