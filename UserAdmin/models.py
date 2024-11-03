from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(
        max_length=12,
    )
    profile_picture_url = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
