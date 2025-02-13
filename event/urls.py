from django.urls import path, include
from event.views import test_file

urlpatterns = [
    path('test-file/', test_file),
]