from django.urls import path
from event.views import dashboard, event_details, create_event, delete_event, update_event, create_category, delete_category,update_category, homepage
from users.views import create_participant, delete_participant, update_participant, participant_list
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('event-detials/<int:id>/', event_details, name='event_details'),
    # path('management/', management, name='management'),

    path('create-event/', create_event, name='create-event'),
    path('delete-event/<event_id>/', delete_event, name='delete-event'),
    path('update-event/<event_id>/', update_event, name='update-event'),

    path('create-category/', create_category, name='create-category'),
    path('delete-category/<category_id>/', delete_category, name='delete-category'),
    path('update-category/<category_id>/', update_category, name='update-category'),

    path('create-participant/', create_participant, name='create-participant'),
    path('delete-participant/', delete_participant, name='delete-participant'),
    path('update-participant/', update_participant, name='update-participant'),

    path('participant-list/', participant_list, name='participant-list')
]