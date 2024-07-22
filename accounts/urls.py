"""Defines URL patterns for accounts."""
from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    path('new_profile/', views.new_profile, name='new_profile'),
]
