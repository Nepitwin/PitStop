from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/events", views.ajax_events, name="api/events"),
]
