from zoneinfo import ZoneInfo

import fastf1
from django.conf import settings
from django.shortcuts import render
from pitstop.service.formula_api import FormulaApi

def index(request):

    # Enable the cache for performance improvements
    fastf1.Cache.enable_cache(settings.BASE_DIR)

    schedule = fastf1.get_event_schedule(2025, include_testing=False)
    events = FormulaApi.get_all_events_from_year(schedule)
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
        'events': events,
        'driver_standings': driver_df.to_dict(orient='records'),
        'constructor_standings': constructor_df.to_dict(orient='records'),
    }

    return render(request, "race_events.html", context)
