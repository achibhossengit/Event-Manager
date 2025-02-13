from django.urls import path, include
from event.views import test_view

urlpatterns = [
    path('test', test_view),
]