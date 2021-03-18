from src.dto.Date import Date
from src.dto.DateRange import DateRange
from src.dto.Place import Place
from src.dto.PriceRange import PriceRange


class Event:
    score = 100
    description = None
    target_url = None
    source_url = None
    category = None

    def __init__(self, title, date: DateRange, times, place: Place, price_range: PriceRange, container, small_container):
        self.title = title
        self.date = date
        self.times = times
        self.place = place
        self.priceRange = price_range
        self.container = container
        self.small_container = small_container
