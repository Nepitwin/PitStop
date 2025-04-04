from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class TimeApi:

    @staticmethod
    def is_same_week(event_date: datetime, check_date: datetime) -> bool:

        # Get the Monday of the event's week
        event_week_start = event_date - timedelta(days=event_date.weekday())
        event_week_end = event_week_start + timedelta(days=6)

        # Check if the check_date is within the same week
        return event_week_start <= check_date <= event_week_end


    @staticmethod
    def convert_to_timezone(event_date: datetime, zone: ZoneInfo) -> datetime:
        return event_date.astimezone(zone)
