from django.contrib import admin
from .models import AssetData, TransactionData

# Register your models here.
admin.site.register(AssetData)
admin.site.register(TransactionData)
