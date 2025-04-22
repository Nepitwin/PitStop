from datetime import datetime
from typing import List
from pitstop.model.RaceSession import RaceSession


class RaceEvent:

    def __init__(self, session: int, name: str, location: str, date: datetime, sessions: List[RaceSession]):
        self.session = session
        self.name = name
        self.location = location
        self.date = date
        self.sessions = sessions
        self.active = False