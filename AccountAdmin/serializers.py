from rest_framework import serializers
from .models import AccountProfile


class UserNamePublicKeySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')  # Fetch the username from the related User model
    public_key = serializers.CharField(source='public_address')  # Map public_address to public_key

    class Meta:
        model = AccountProfile
        fields = ['name', 'public_key']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = ['user', 'private_address', 'public_address']
        extra_kwargs = {
            'private_address': {'write_only': True},  # Only write on creation
        }

    def create(self, validated_data):
        # Handle the private_address field only during creation
        private_address = validated_data.pop('private_address', None)
        instance = super().create(validated_data)

        # Set the private_address only on creation
        if private_address:
            instance.private_address = private_address
            instance.save()

        return instance

    def to_representation(self, instance):
        # Exclude private_address from representation to make it non-readable
        representation = super().to_representation(instance)
        representation.pop('private_address', None)
        return representation
