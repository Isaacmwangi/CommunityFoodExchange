# accounts/urls.py

from django.urls import path
from .views import UserLoginView, UserLogoutView, user_signup, profile_create, profile_update
from .views import home

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', user_signup, name='signup'),
    path('profile/create/', profile_create, name='profile_create'),
    path('profile/update/', profile_update, name='profile_update'),
    path('', home, name='home'),
]
