import fastf1
from django.conf import settings

class FormulaApi:

    def __init__(self):
        # Enable the cache for performance improvements
        fastf1.Cache.enable_cache(settings.BASE_DIR)
        pass

    def get_all_events_from_year(self, year: int) -> list[dict]:

        events = []

        schedule = fastf1.get_event_schedule(year, include_testing=False)

        # Iterate through all events and print details
        for _, event in schedule.iterrows():
            events.append({
                "round": event['RoundNumber'],
                "name": event['EventName'],
                "location": f"{event['Location']} - {event['Country']}",
                "date": event['EventDate'],
                "sessions": {
                    event['Session1']: event['Session1Date'],
                    event['Session2']: event['Session2Date'],
                    event['Session3']: event['Session3Date'],
                    event['Session4']: event['Session4Date'],
                    event['Session5']: event['Session5Date'],
                }
            })

        return events