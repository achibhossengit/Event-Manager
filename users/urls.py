from django.urls import path
from users.views import sign_up, log_in, log_out

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('log-in/', log_in, name='log-in'),
    path('log-out/', log_out, name='log-out'),
]