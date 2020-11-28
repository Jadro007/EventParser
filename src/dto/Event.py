from src.dto.Date import Date
from src.dto.Place import Place
from src.dto.PriceRange import PriceRange


class Event:
    def __init__(self, title, date: Date, time, place: Place, price_range: PriceRange, container):
        self.title = title
        self.date = date
        self.time = time
        self.place = place
        self.priceRange = price_range
        self.container = container
