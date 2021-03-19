import json
from typing import List

from src.dto.Event import Event


class EventsJSONSerializer:

    @staticmethod
    def serialize(events: List[Event]):
        results = []
        for event in events:

            price_from_value = ""
            if event.priceRange is not None:
                price_from_value = event.priceRange.priceFrom.value

            price_to_value = ""
            if event.priceRange is not None:
                price_to_value = event.priceRange.priceTo.value

            alternative_title_value = event.title.alternative_value
            if event.title.value == event.title.alternative_value:
                alternative_title_value = ""

            description = ""
            if event.description is not None:
                description = event.description.value

            target_url = ""
            if event.target_url is not None:
                target_url = event.target_url

            source_url = ""
            if event.source_url is not None:
                source_url = event.source_url

            time_value = ""
            if event.times is not None:
                if len(event.times) > 1:
                    time_value = event.times[0].value + " - " + event.times[-1].value
                elif len(event.times) > 0:
                    time_value = event.times[0].value

            category = ""
            if event.category is not None:
                category = event.category

            tags = ""
            if event.tags is not None:
                tags = event.tags


            results.append({
                "title":  event.title.value,
                "alternativeTitle":  alternative_title_value,
                "dateFrom": event.date.dateFrom.datetime.strftime("%Y-%m-%d"),
                "dateTo": event.date.dateTo.datetime.strftime("%Y-%m-%d"),
                "time": time_value,
                "place": event.place.city,
                "priceFrom": price_from_value,
                "priceTo": price_to_value,
                "score": event.score,
                "description": description,
                "target_url": target_url,
                "source_url": source_url,
                "category": category,
                "tags": tags
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return json.dumps(results, ensure_ascii=False)
