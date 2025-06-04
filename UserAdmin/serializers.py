import os
import base64
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from eth_account import Account
from AccountAdmin.models import AccountProfile

try:
    from cryptography.fernet import Fernet, InvalidToken
    _CRYPT_AVAILABLE = True
except ImportError:
    _CRYPT_AVAILABLE = False
    # Fallback to weak encoding below if cryptography is unavailable

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

    def _get_encryption_key(self):
        key = os.environ.get('ETH_PRIVATE_KEY_SECRET')
        if not key:
            raise RuntimeError(
                "Encryption key for Ethereum private keys ('ETH_PRIVATE_KEY_SECRET') not set in environment variables."
            )
        # Fernet expects a 32-byte urlsafe base64-encoded key
        if _CRYPT_AVAILABLE:
            try:
                _ = base64.urlsafe_b64decode(key)
            except Exception:
                raise RuntimeError("ETH_PRIVATE_KEY_SECRET must be a urlsafe_base64-encoded 32-byte key for Fernet.")
            if len(base64.urlsafe_b64decode(key)) != 32:
                raise RuntimeError("ETH_PRIVATE_KEY_SECRET must decode to 32 bytes.")
        else:
            # Fallback: Just use the key bytes (not secure, handled in fallback methods)
            pass
        return key

    def _encrypt_private_key(self, private_key_hex: str) -> str:
        """
        Encrypt the private key using symmetric encryption (Fernet).
        Returns the encrypted value as a string.
        """
        key = self._get_encryption_key()
        if _CRYPT_AVAILABLE:
            f = Fernet(key)
            # private_key_hex is already a string, but Fernet wants bytes
            token = f.encrypt(private_key_hex.encode('utf-8'))
            return token.decode('utf-8')
        else:
            # Fallback: very weak "encryption" (XOR with key bytes and base64)
            # Not cryptographically secure! Just obfuscation. Replace with proper cryptography in prod.
            key_bytes = key.encode('utf-8')
            pk_bytes = private_key_hex.encode('utf-8')
            xored = bytes([a ^ key_bytes[i % len(key_bytes)] for i, a in enumerate(pk_bytes)])
            return base64.urlsafe_b64encode(xored).decode('utf-8')

    def _decrypt_private_key(self, encrypted_value: str) -> str:
        """
        Decrypt the private key. Call this wherever reading from DB.
        """
        key = self._get_encryption_key()
        if _CRYPT_AVAILABLE:
            f = Fernet(key)
            try:
                plain = f.decrypt(encrypted_value.encode('utf-8'))
            except InvalidToken:
                raise RuntimeError('Invalid encryption token or key when decrypting Ethereum private key.')
            return plain.decode('utf-8')
        else:
            key_bytes = key.encode('utf-8')
            cipher_bytes = base64.urlsafe_b64decode(encrypted_value.encode('utf-8'))
            plain_bytes = bytes([a ^ key_bytes[i % len(key_bytes)] for i, a in enumerate(cipher_bytes)])
            return plain_bytes.decode('utf-8')

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

        encrypted_private_key = self._encrypt_private_key(private_key)
        account_profile = AccountProfile.objects.create(user=user, private_address=encrypted_private_key,
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