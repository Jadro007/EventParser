from src.dto.DateGroup import DateGroup


class Date:
    def __init__(self, datetime, realValue, container):
        self.datetime = datetime
        self.realValue = realValue
        self.container = container
        self.group = None

    def set_group(self, group: DateGroup):
        self.group = group

