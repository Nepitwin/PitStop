from datetime import datetime
from zoneinfo import ZoneInfo


class TimeApi:
    @staticmethod
    def convert_to_timezone(event_date: datetime, zone: ZoneInfo) -> datetime:
        return event_date.astimezone(zone)
