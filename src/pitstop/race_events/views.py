from zoneinfo import ZoneInfo
from django.shortcuts import render
from pitstop.service.formula_api import FormulaApi

def index(request):
    return render(request, "race_events.html")

def ajax_events(request):
    schedule = FormulaApi.get_event_schedule(2025, include_testing=False)
    events = FormulaApi.get_all_race_events(schedule)
    driver_df, constructor_df = FormulaApi.get_standings(schedule)

    # Convert all session dates to the specified timezone
    zone = ZoneInfo("Europe/Berlin")
    for event in events:
        for session in event.sessions:
            session.date = session.date.astimezone(zone)

    # Get next event as active event
    event = FormulaApi.get_next_event(events)
    if event:
        event.active = True

    context = {
        "events": events,
        "driver_standings": driver_df.to_dict(orient="records"),
        "constructor_standings": constructor_df.to_dict(orient="records"),
    }

    return render(request, "events.html", context)
