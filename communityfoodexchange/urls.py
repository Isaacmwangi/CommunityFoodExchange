"""
URL configuration for communityfoodexchange project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# communityfoodexchange/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    path('listings/', include('listings.urls')),  # Include the listings URLs
    path('exchange/', include('exchange.urls')),  # Include the exchange URLs
    path('messaging/', include('messaging.urls')),  # Include the messaging URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Define the handler404 view
handler404 = 'accounts.views.custom_404_view'

# Customize Django administration
admin.site.site_header = "FreshHarvest Community Exchange"  # Change the admin header
admin.site.site_title = "FreshHarvest Community Exchange"  # Change the admin title

