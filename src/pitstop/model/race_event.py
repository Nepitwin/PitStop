from dataclasses import dataclass
from datetime import datetime
from typing import List
from pitstop.model.race_session import RaceSession

@dataclass
class EventInfo:
    session: int
    name: str
    location: str
    date: datetime
    sessions: List['RaceSession']

class RaceEvent:

    def __init__(self, info: EventInfo):
        self.session = info.session
        self.name = info.name
        self.location = info.location
        self.date = info.date
        self.sessions = info.sessions
        self.active = False
        self.finished = False
