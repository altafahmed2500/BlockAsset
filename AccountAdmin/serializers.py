from rest_framework import serializers
from .models import AccountProfile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = ['user', 'private_address', 'wallet_address']
        extra_kwargs = {
            'private_address': {'write_only': True},  # Hide the private address in responses
        }
