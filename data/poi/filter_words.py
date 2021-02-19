import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
with open("./cz_dic/Czech.3-2-5.dic", encoding="windows-1250") as f:
    content = f.readlines()

content = [x.strip() for x in content]

with open("./poi.txt", encoding="utf-8") as f:
    poi = f.readlines()

poi = [x.strip() for x in poi]

result = []

print ("started", flush=True)
i = 0
with open("poi_final.txt", "a", encoding="utf-8") as f:
    for p in poi:
        i += 1
        found_poi = False
        print(str(i) + " / " + str(len(poi)) + "\n", flush=True)
        for line in content:
            if p.lower() == line.lower():
                found_poi = True
                print("Found " + p + " - it will be ignored\n", flush=True)
                break
        if found_poi is False:
            print(p + " is valid \n", flush=True)
            f.write(p + "\n")





