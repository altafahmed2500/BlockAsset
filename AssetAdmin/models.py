import uuid
from django.contrib.auth.models import User
from django.db import models


class AssetData(models.Model):
    asset_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    asset_hash = models.CharField(
        max_length=64
    )
    asset_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assets'
    )  # Many-to-one: One user can own many assets
    ipfs_hash = models.CharField(
        max_length=64,
        null=True
    )
    transaction_id = models.CharField(
        max_length=64,
        null=True
    )
    token_id = models.CharField(
        max_length=64,
        null=True
    )
    file_id = models.ForeignKey(
        'FileAdmin.FileData',
        on_delete=models.CASCADE,
        related_name='assets'
    )  # Many-to-one: One file can be linked to many assets
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Asset ID: {self.asset_id}, Owner: {self.asset_owner.username}, File ID: {self.file_id}"


from django.db import models

# Create your models here.
