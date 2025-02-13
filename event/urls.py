from django.urls import path, include
from event.views import create_event

urlpatterns = [
    path('create-event', create_event, name='event_creations')
]