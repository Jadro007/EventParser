import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

with open("./poi_final.txt", encoding="utf-8") as f:
    poi = f.readlines()

poi = [x.strip() for x in poi]

result = []

print ("started", flush=True)
i = 0

def is_float(value):
  try:
    int(value)
    return True
  except:
    return False


with open("poi_final_filtered.txt", "w", encoding="utf-8") as f:
    for p in poi:

        if is_float(p):
            print(p + " is float\n", flush=True)
            continue

        if len(p) < 5:
            print(p + "is too short")
            continue

        f.write(p + "\n")





