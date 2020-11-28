from src.dto.Price import Price


class PriceRange:
    def __init__(self, price_from: Price, price_to: Price, container):
        self.priceFrom = price_from
        self.priceTo = price_to
        self.container = container
