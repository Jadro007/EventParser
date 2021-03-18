#!/usr/bin/env python3

import subprocess
import os
import tempfile
import time

start_time = time.time()

urls = [
    "https://bandzone.cz/thefialky?at=gig",
    "https://bandzone.cz/koncert/514758-ceske-budejovice-mc-fabrika-zavis-v-ceskych-budejovicich",
    "https://www.benatska.cz/",
    "https://www.ticketlive.cz/cs/event/vysocina-fest-8-10-7-2021",
    "https://www.deratizeri.cz/der08/index.php?show=koncerty",
    "https://www.informuji.cz/akce/vikend/",
    "https://goout.net/cs/mig-21/pzwte/",
    "https://goout.net/cs/mig-21/szvlfpq/",
    "https://www.ticketportal.cz/event/Killer-Queen-UK",
    "https://www.ticketstream.cz/tickets/skwor-0"
]

processes = []
for url in urls:
    f = tempfile.TemporaryFile()
    print("Starting url: " + url, flush=True)
    p = subprocess.Popen(['python3', 'run.py', url], stdout=f)
    processes.append((p, f))
    print("Waiting", flush=True)
    # p.wait()


for p, f in processes:
    p.wait()
    f.seek(0)
    print(f.read())
    f.close()

print("--- %s seconds ---" % (time.time() - start_time))
