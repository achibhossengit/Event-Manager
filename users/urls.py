from django.urls import path
from users.views import sign_up, log_in, log_out, no_permission, delete_user, update_user, user_details, create_group, update_group, delete_group

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('log-in/', log_in, name='log-in'),
    path('log-out/', log_out, name='log-out'),
    path('no-permission/', no_permission, name='no-permission'),
    path('delete-user/<user_id>/', delete_user, name='delete-user'),
    path('update-user/<user_id>/', update_user, name='update-user'),
    path('user-details/<user_id>', user_details, name='user-details'),
    path('create-group/', create_group, name='create-group'),
    path('update-group/<group_id>/', update_group, name='update-group'),
    path('delete-group/<group_id>/', delete_group, name='delete-group'),
]