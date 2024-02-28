# accounts/urls.py

from django.urls import path
from .views import UserLoginView, user_signup, profile_create, profile_update, user_logout, profile, home
from listings.views import listing_create

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/create/', profile_create, name='profile_create'),
    path('profile/update/', profile_update, name='profile_update'),
    path('', home, name='home'),
    path('listings/create/', listing_create, name='listing_create'),
]


