from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars/')
    bio = models.TextField(max_length=500, blank=True)
