from zoneinfo import ZoneInfo
from asgiref.sync import sync_to_async
from django.shortcuts import render
from pitstop.service.formula_api import FormulaApi

async def index(request):

    schedule = await sync_to_async(FormulaApi.get_event_schedule)(2025, include_testing=False)
    events = await sync_to_async(FormulaApi.get_all_events_from_year)(schedule)
    driver_df, constructor_df = await sync_to_async(FormulaApi.get_standings)(schedule)

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
