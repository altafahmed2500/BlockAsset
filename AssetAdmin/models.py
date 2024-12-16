import uuid
from django.contrib.auth.models import User
from django.db import models


class AssetData(models.Model):
    asset_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    block_number = models.CharField(
        max_length=64
    )
    transaction_id = models.CharField(
        max_length=64
    )
    token_id = models.CharField(
        max_length=64
    )
    asset_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assets'
    )  # Many-to-one: One user can own many assets
    file_id = models.ForeignKey(
        'FileAdmin.FileData',
        on_delete=models.CASCADE,
        related_name='assets'
    )  # Many-to-one: One file can be linked to many assets
    name = models.CharField(
        max_length=255,
        null=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )


class TransactionData(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    from_address = models.CharField(
        max_length=255,
        null=False
    )
    to_address = models.CharField(
        max_length=255,
        null=False
    )
    time = models.DateTimeField(
        auto_now_add=True
    )
    transaction_hash = models.CharField(
        max_length=64,
        unique=True
    )
    block_number = models.CharField(
        max_length=64
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
