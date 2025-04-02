from django.shortcuts import render

def index(request):
    events = [
        {
            "round": 23,
            "name": "Qatar Grand Prix",
            "location": "Lusail - Qatar",
            "sessions": {
                "Practice 1": "2024-11-29 16:30:00+03:00",
                "Sprint Qualifying": "2024-11-29 20:30:00+03:00",
                "Sprint": "2024-11-30 17:00:00+03:00",
                "Qualifying": "2024-12-07 18:00:00+04:00",
                "Race": "2024-12-01 19:00:00+03:00"
            }
        },
        {
            "round": 24,
            "name": "Abu Dhabi Grand Prix",
            "location": "Yas Island - UAE",
            "sessions": {
                "Practice 1": "2024-12-06 13:30:00+04:00",
                "Practice 2": "2024-12-06 17:00:00+04:00",
                "Practice 3": "2024-12-07 14:30:00+04:00",
                "Qualifying": "2024-12-07 18:00:00+04:00",
                "Race": "2024-12-08 17:00:00+04:00"
            }
        }
    ]

    context = {"events": events}
    return render(request, "race_events.html", context)
