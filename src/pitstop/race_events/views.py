from django.shortcuts import render
from zoneinfo import ZoneInfo

from pitstop.model.RaceSession import RaceSession
from pitstop.service.TimeApi import TimeApi
from pitstop.service.FormulaApi import FormulaApi

def index(request):
    events = FormulaApi.get_all_events_from_year(2025)
    zone = ZoneInfo("Europe/Berlin")

    for event in events:
        for session in event.sessions:
            _convert_timezone_from_session(session, zone)

    event = FormulaApi.get_next_event(events)
    if event:
        event.active = True

    return render(request, "race_events.html", {"events": events})

def _convert_timezone_from_session(session: RaceSession, zone: ZoneInfo):
    session.date = TimeApi.convert_to_timezone(session.date, zone)