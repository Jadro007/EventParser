import io
import sys
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

categories = {}
with open("./nlp/ner/categories.txt", encoding="utf-8") as f:
    csv_reader = csv.reader(f, delimiter='|')
    for row in csv_reader:
        categories[row[1]] = True


i = 0
with open("categories_list.txt", "a", encoding="utf-8") as f:
    for category in categories:

        print(category + " is valid \n", flush=True)
        f.write(category + "\n")





