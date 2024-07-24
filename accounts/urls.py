"""Defines URL patterns for accounts."""
from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    path('delete/', views.delete, name='delete'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:id>/', views.profile, name='profile'),
]
