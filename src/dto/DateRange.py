from src.dto.Date import Date


class DateRange:
    def __init__(self, date_from: Date, date_to: Date, container):
        self.dateFrom = date_from
        self.dateTo = date_to
        self.container = container
