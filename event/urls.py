from django.urls import path
from event.views import dashboard, event_details, management_events, management_categories, management_participants, create_event, delete_event, update_event, create_category, delete_category,update_category, create_participant, delete_participant, update_participant, homepage, participant_list
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('event-detials/<int:id>/', event_details, name='event_details'),
    # path('management/', management, name='management'),
    path('management-events', management_events, name='management-events'),
    path('management-categories', management_categories, name='management-categories'),
    path('management-participants', management_participants, name='management-participants'),

    path('create-event/', create_event, name='create-event'),
    path('delete-event/', delete_event, name='delete-event'),
    path('update-event/', update_event, name='update-event'),

    path('create-category/', create_category, name='create-category'),
    path('delete-category/', delete_category, name='delete-category'),
    path('update-category/', update_category, name='update-category'),

    path('create-participant/', create_participant, name='create-participant'),
    path('delete-participant/', delete_participant, name='delete-participant'),
    path('update-participant/', update_participant, name='update-participant'),

    path('participant-list/', participant_list, name='participant-list')
]