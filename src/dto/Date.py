from src.dto.DateGroup import DateGroup


class Date:
    def __init__(self, datetime, realValue, container, is_year_guessed=False):
        self.datetime = datetime
        self.realValue = realValue
        self.container = container
        self.group = None
        self.isYearGuessed = is_year_guessed

    def set_group(self, group: DateGroup):
        self.group = group

