from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from eth_account import Account
from AccountAdmin.models import AccountProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    # Nested User fields for GET request (read-only)
    user = UserSerializer(read_only=True)

    # Fields for POST request (write-only)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',  # Returned in GET
            'phone_number', 'profile_picture_url', 'date_of_birth',
            'first_name', 'last_name', 'email', 'username', 'password',  # Required in POST
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Extract user data from the validated data
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        # Create the User instance
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password  # Ensure password is hashed
        )
        eth_account = Account.create()
        public_address = eth_account.address
        private_key = eth_account.key.hex()
        account_profile = AccountProfile.objects.create(user=user, private_address=private_key,
                                                        public_address=public_address)
        # Create the UserProfile associated with the newly created user
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
