from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from eth_account import Account
from AccountAdmin.models import AccountProfile

import base64
import hashlib
import os
from django.conf import settings

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Helper functions for key derivation and encryption
def _derive_key(secret, length=32):
    # Derive a key from the Django SECRET_KEY using SHA-256
    return hashlib.sha256(secret.encode('utf-8')).digest()[:length]

def aes_encrypt(plaintext, key):
    # AES-256 CBC with PKCS7 padding
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext.encode('utf-8'), AES.block_size)
    ct = cipher.encrypt(padded)
    return base64.b64encode(iv + ct).decode('utf-8')

def aes_decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext)
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')


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

        # Encrypt the private key before storing
        encryption_key = _derive_key(settings.SECRET_KEY)
        encrypted_private_key = aes_encrypt(private_key, encryption_key)

        account_profile = AccountProfile.objects.create(
            user=user,
            private_address=encrypted_private_key,  # Store ENCRYPTED private key
            public_address=public_address
        )
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