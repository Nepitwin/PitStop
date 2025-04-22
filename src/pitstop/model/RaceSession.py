from datetime import datetime

class RaceSession:

    def __init__(self, name: str, date: datetime):
        self.name = name
        self.date = date

    def date_to_string(self) -> str:
        return str(self.date)