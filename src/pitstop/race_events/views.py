from zoneinfo import ZoneInfo
from django.shortcuts import render
from pitstop.service.formula_api import FormulaApi

def index(request):
    events = FormulaApi.get_all_events_from_year(2025)

    # Convert all session dates to the specified timezone
    zone = ZoneInfo("Europe/Berlin")
    for event in events:
        for session in event.sessions:
            session.date = session.date.astimezone(zone)

    # Get next event as active event
    event = FormulaApi.get_next_event(events)
    if event:
        event.active = True

    return render(request, "race_events.html", {"events": events})
