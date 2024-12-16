from rest_framework import serializers
from .models import AssetData


class AssetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetData
        fields = [
            'asset_id',
            'block_number',
            'transaction_id',
            'token_id',
            'name',
            'file_id',
            'created_at'
        ]
