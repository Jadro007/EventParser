## POI

This part of projects uses POI from OpenStreetMaps.
Main output for EventParser is list of places (POIs) that are suitable to host event.
This was achieved by downloading all places in Czechia (https://wiki.openstreetmap.org/wiki/Planet.osm, not included in this repo because it is around 12GB unpacked),
converted to osm xml format using osmconvert.exe and filtered to find proper tags using osmfilter.exe.
Then it ran through list of all Czech words (cz_dic) to remove places that were in the list to not have false positive events found by Event Parser.
Also all POIs with length less then 5 characters were removed to lessen this noise (parse_osm.py and filter_words.py).