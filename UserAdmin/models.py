import uuid

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


class UserConnection(models.Model):
    follower = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Incident(models.Model):
    incident_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,  # Generates a unique identifier
        editable=False
    )
    user = models.ForeignKey(
        User,  # Connects the incident to a user
        on_delete=models.CASCADE,
        related_name='incidents'
    )
    incident_name = models.CharField(
        max_length=255,
        verbose_name="Incident Name"
    )
    incident_description = models.TextField(
        verbose_name="Incident Description",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
