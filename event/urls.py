from django.urls import path, include
from event.views import test_view, dashboard, event_details, management, create_event, delete_event, update_event, create_category, delete_category,update_category, create_participant, delete_participant, update_participant
urlpatterns = [
    path('test', test_view),
    path('dashboard/', dashboard, name='dashboard'),
    path('event-detials/<int:id>', event_details, name='event_details'),
    path('management', management, name='management'),

    path('create-event', create_event, name='create-event'),
    path('delete-event', delete_event, name='delete-event'),
    path('update-event', update_event, name='update-event'),

    path('create-category', create_category, name='create-category'),
    path('delete-category', delete_category, name='delete-category'),
    path('update-category', update_category, name='update-category'),

    path('create-participant', create_participant, name='create-participant'),
    path('delete-participant', delete_participant, name='delete-participant'),
    path('update-participant', update_participant, name='update-participant'),
]