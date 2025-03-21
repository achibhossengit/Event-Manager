from django.urls import path
from event.views import dashboard, event_details, update_category, book_event, CreateEvent, DeleteEvent, UpdateEvent, CreateCategory, DeleteCategory
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('event-detials/<int:id>/', event_details, name='event-details'),

    path('create-event/', CreateEvent.as_view(), name='create-event'),
    path('delete-event/<event_id>/', DeleteEvent.as_view(), name='delete-event'),
    path('update-event/<event_id>/', UpdateEvent.as_view(), name='update-event'),

    path('create-category/', CreateCategory.as_view(), name='create-category'),
    path('delete-category/<category_id>/', DeleteCategory.as_view(), name='delete-category'),
    path('update-category/<category_id>/', update_category, name='update-category'),

    path('book-event/<event_id>/', book_event, name='book-event'),
]