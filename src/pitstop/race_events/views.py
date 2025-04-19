from datetime import datetime
from django.shortcuts import render
from zoneinfo import ZoneInfo

from pitstop.service.TimeApi import TimeApi
from pitstop.service.FormulaApi import FormulaApi

def index(request):
    events = FormulaApi.get_all_events_from_year(2025)

    counter = 0
    active_counter = 0
    current_date = datetime.today()

    zone = ZoneInfo("Europe/Berlin")

    for event in events:
        event["active"] = False

        sessions = event["sessions"]
        for key in sessions.keys():
            # Transfer all events to local time
            sessions[key] = str(TimeApi.convert_to_timezone(sessions[key], zone))

        if TimeApi.is_same_week(current_date, event["date"]):
            active_counter = counter

        counter += 1

    events[active_counter]["active"] = True

    return render(request, "race_events.html", {"events": events})

