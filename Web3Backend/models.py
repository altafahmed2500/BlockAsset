import uuid

from django.db import models


# Create your models here.
class ContractProfile(models.Model):
    contract_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    contract_address = models.CharField(
        max_length=64,
        null=True
    )
    contract_abi = models.TextField(
    )
    contract_bytecode = models.TextField(
    )
    owner_address = models.CharField(
        max_length=64,
        null=True
    )
