# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    UserLoginView,
    user_signup,
    profile_create,
    profile_update,
    user_logout,
    profile,
    home,
    update_username,
    change_password,
    send_password_reset_email,  
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/create/', profile_create, name='profile_create'),
    path('profile/update/', profile_update, name='profile_update'),
    path('username/update/', update_username, name='update_username'),  # New URL for username update
    path('password/change/', change_password, name='change_password'),  # New URL for password change
    path('', home, name='home'),
    path('send_password_reset_email/', send_password_reset_email, name='send_password_reset_email'),

    # Password Reset URLs
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),

    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]