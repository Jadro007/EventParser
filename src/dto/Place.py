class Place:
    is_external_place = False
    is_forced = False

    def __init__(self, city, container):
        self.city = city
        self.container = container
