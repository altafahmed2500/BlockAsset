import hashlib
from rest_framework import serializers
from .models import FileData
from AccountAdmin.models import AccountProfile


class FileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileData
        fields = ['file_id', 'file_path', 'file_hash', 'file_metadata', 'created_at', 'updated_at', 'user_address']
        read_only_fields = ['file_id', 'file_hash', 'file_metadata', 'created_at', 'updated_at', 'user_address']

    def __init__(self, *args, request=None, **kwargs):
        super(FileDataSerializer, self).__init__(*args, **kwargs)
        self.request = request

    def create(self, validated_data):
        # Use self.get_user_info() to get the user's public address
        user_info = self.get_user_info()
        user_address = user_info['public_address'] if user_info else None

        # Extract the uploaded file
        file = validated_data.get('file_path')

        # Compute file hash (SHA-256)
        file_hash = self._generate_file_hash(file)

        # Automatically generate file metadata
        file_metadata = {
            "file_name": file.name,
            "file_size": file.size,
            "file_type": file.content_type,
        }

        # Add the generated metadata to validated data
        validated_data['file_hash'] = file_hash
        validated_data['file_metadata'] = file_metadata
        validated_data['user_address'] = user_address

        # Save and return the FileData object
        return super().create(validated_data)

    def _generate_file_hash(self, file):
        # Compute SHA-256 hash of the uploaded file
        hasher = hashlib.sha256()
        for chunk in file.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

    def get_user_info(self):
        user = self.request.user  # The user is automatically populated based on the token
        try:
            account_profile = user.account_profile  # Using the related name to get the AccountProfile
            public_address = account_profile.public_address
        except AccountProfile.DoesNotExist:
            print("This user does not have an associated account profile.")
            public_address = None  # Set to None if no profile exists

        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "public_address": public_address,
        }
        return user_data
