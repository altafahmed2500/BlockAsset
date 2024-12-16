from django.urls import path
from .views import get_total_assets, create_token_api, transfer_token_api, recent_transactions_api, \
    all_transactions_api, update_metadata_upload_create_asset, check_asset, get_user_files_with_assets, \
    get_user_asset_count, get_user_assets

urlpatterns = [
    path('count', get_total_assets, name='asset-count'),
    path('createToken', create_token_api, name='create_token_api'),
    path('transferToken', transfer_token_api, name='transfer_token'),
    path('recentTransactions', recent_transactions_api, name='recent-transactions'),
    path('userTransactions', all_transactions_api, name="all-user-transaction"),
    path('updateuploadcreate', update_metadata_upload_create_asset, name="update_metadata_upload_create_asset"),
    path('checkAsset', check_asset, name='check_asset'),
    path('getUserFilesWithAssets', get_user_files_with_assets, name='get_user_files_with_assets'),
    path('userassetcount', get_user_asset_count, name='get_user_asset_count'),
    path('userassets', get_user_assets, name='get_user_assets')
]
