from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AccountProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_profile')
    private_address = models.CharField(
        max_length=255,
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$', message='This is the hash of the private key')]
    )
    public_address = models.CharField(
        max_length=255,
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$', message='Wallet address must be alphanumeric.')]
    )
