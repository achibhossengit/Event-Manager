from django.urls import path, include
from event.views import test_view, dashboard

urlpatterns = [
    path('test', test_view),
    path('dashboard', dashboard, name='dashboard'),
]