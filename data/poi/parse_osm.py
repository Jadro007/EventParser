from lxml import etree

i = 1

while i <= 30:

    tree = etree.parse("amenity/"+str(i)+".osm")

    names = tree.xpath("//osm/way/tag[@k=\"name\"]/@v")
    i += 1
    print("yay")
    with open("poi.txt", "a", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")





