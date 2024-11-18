from django.db import models
import uuid

from AccountAdmin.models import AccountProfile


class FileData(models.Model):
    file_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file_path = models.FileField(
        upload_to='uploads/'
    )
    file_hash = models.CharField(
        max_length=64
    )
    file_hash_updated = models.CharField(
        max_length=64,
        null=True
    )
    ipfs_hash = models.CharField(
        max_length=64,
        null=True
    )
    file_metadata = models.JSONField()

    user_address = models.CharField(
        max_length=64,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
