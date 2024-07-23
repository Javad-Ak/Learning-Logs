from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        labels = {'username': 'Username', 'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email',
                  'password': 'Password'}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        labels = {'avatar': 'Avatar', 'bio': 'Bio'}
        enctype = 'multipart/form-data'
