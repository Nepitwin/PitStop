from django.shortcuts import render
from pitstop.service.FormulaApi import FormulaApi

def index(request):
    api = FormulaApi()
    events = api.get_all_events_from_year(2025)
    context = {"events": events}
    return render(request, "race_events.html", context)
