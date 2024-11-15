import hashlib
from rest_framework import serializers
from .models import FileData
from AccountAdmin.models import AccountProfile
from rest_framework.exceptions import ValidationError
from .updateMetaData import addCustomMetadataToPdf


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

        # Check if a file with the same hash already exists
        if FileData.objects.filter(file_hash=file_hash).exists():
            raise ValidationError("A file with this hash already exists.")

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
    # def update(self, instance, validated_data):
    #     file_path =
    #     file = validated_data.get('file_path', None)
    #     user_info = self.get_user_info()
    #     user_address = user_info['public_address'] if user_info else None
    #     user_name = user_info['username'] if user_info else None
    #
    #     # Check if a new file is uploaded
    #     if new_file and new_file != instance.file_path:
    #         new_file_hash = self._generate_file_hash(new_file)
    #
    #         # Ensure the new hash is unique in the database
    #         if FileData.objects.filter(file_hash=new_file_hash).exclude(file_id=instance.file_id).exists():
    #             raise ValidationError("A file with this hash already exists.")
    #
    #         # Update the file hash and metadata only if the file has changed
    #         instance.file_hash = new_file_hash
    #         instance.file_metadata = {
    #             "file_name": new_file.name,
    #             "file_size": new_file.size,
    #             "file_type": new_file.content_type,
    #         }
    #         instance.file_path = new_file
    #
    #     # Update other fields if they are provided in the validated data
    #     instance.file_hash_updated = validated_data.get('file_hash_updated', instance.file_hash_updated)
    #     instance.user_address = validated_data.get('user_address', instance.user_address)
    #
    #     instance.save()
    #     return instance

