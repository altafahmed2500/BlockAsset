from rest_framework import serializers
from .models import AccountProfile


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
