from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView
from users.views import sign_up, log_in, log_out, no_permission, delete_user, update_user, user_details, create_group, update_group, delete_group, active_user, ProfileView, EditProfile, ChangePassword, CustomPasswordReset, CustomPasswordResetConfirmView

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('activate/<int:user_id>/<str:token>', active_user),
    path('log-in/', log_in, name='log-in'),
    path('log-out/', log_out, name='log-out'),
    path('no-permission/', no_permission, name='no-permission'),
    path('delete-user/<user_id>/', delete_user, name='delete-user'),
    path('update-user/<user_id>/', update_user, name='update-user'),
    path('user-details/<user_id>', user_details, name='user-details'),
    path('create-group/', create_group, name='create-group'),
    path('update-group/<group_id>/', update_group, name='update-group'),
    path('delete-group/<group_id>/', delete_group, name='delete-group'),

    path('user-profile/', ProfileView.as_view(), name='user-profile'),
    path('edit-profile/', EditProfile.as_view(), name='edit-profile'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('reset-password/', CustomPasswordReset.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]