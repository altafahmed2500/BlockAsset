from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import AssetData, TransactionData
from .asset_operations import create_asset
from AccountAdmin.models import AccountProfile
from FileAdmin.models import FileData
from FileAdmin.updateMetaData import updateMetaData
from FileAdmin.IPFSConnect import add_to_ipfs
from .transfer_token import transfer_token
from django.db import models
from .serializers import AssetDataSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_total_assets(request):
    total_assets = AssetData.objects.count()
    return Response({'total_assets': total_assets})


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def create_token_api(request):
    """
    API to create a new token and save it in the database.
    """
    data = request.data
    ipfs_hash = data.get("ipfs_hash")
    asset_name = data.get("name")

    if not ipfs_hash or not asset_name:
        return JsonResponse({"error": "IPFS hash and name are required"}, status=400)

    try:
        # Get the authenticated user
        user = request.user

        # Retrieve AccountProfile for the user
        try:
            account_profile = AccountProfile.objects.get(user=user)
            account_id = account_profile.public_address
            private_key = account_profile.private_address
        except AccountProfile.DoesNotExist:
            return JsonResponse({"error": "Account profile not found for the user."}, status=404)

        # Retrieve FileData for the given IPFS hash
        try:
            file_data = FileData.objects.get(ipfs_hash=ipfs_hash)
        except FileData.DoesNotExist:
            return JsonResponse({"error": "File not found for the given IPFS hash."}, status=404)

        # Call the create_asset function to interact with the blockchain
        result = create_asset(ipfs_hash, asset_name, account_id, private_key)

        # Save the result to the AssetData table
        asset_data = AssetData.objects.create(
            block_number=result["block_number"],
            transaction_id=result["transaction_id"],
            token_id=result["token_id"],
            asset_owner=user,
            file_id=file_data,
            name=asset_name
        )

        # Save the transaction to the TransactionData table
        TransactionData.objects.create(
            from_address=account_id,
            to_address=result["owner"],  # Assuming `owner` is the recipient address in the response
            transaction_hash=result["transaction_id"],  # Using the blockchain's transaction ID as the hash
            block_number=result["block_number"],
            created_by=user
        )

        # Return the saved data along with the response
        return JsonResponse({
            "asset_id": str(asset_data.asset_id),
            "block_number": asset_data.block_number,
            "transaction_id": asset_data.transaction_id,
            "token_id": asset_data.token_id,
            "asset_owner": asset_data.asset_owner.username,
            "file_id": str(asset_data.file_id.file_id),
            "name": asset_data.name,
            "created_at": asset_data.created_at
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def transfer_token_api(request):
    """
    API to transfer a token to another address and save transaction details in the database.
    """
    data = request.data
    token_id = data.get("token_id")
    to_address = data.get("to_address")

    if not token_id or not to_address:
        return JsonResponse({"error": "Token ID and recipient address are required"}, status=400)

    try:
        # Get the authenticated user
        user = request.user

        # Retrieve AccountProfile for the sender
        try:
            account_profile = AccountProfile.objects.get(user=user)
            account_id = account_profile.public_address
            private_key = account_profile.private_address
        except AccountProfile.DoesNotExist:
            return JsonResponse({"error": "Account profile not found for the user."}, status=404)

        # Retrieve the recipient user (to_address)
        try:
            recipient_profile = AccountProfile.objects.get(public_address=to_address)
            recipient_user = recipient_profile.user
        except AccountProfile.DoesNotExist:
            return JsonResponse({"error": "Recipient account not found."}, status=404)

        # Retrieve the AssetData record for the token_id
        try:
            asset = AssetData.objects.get(token_id=token_id)
        except AssetData.DoesNotExist:
            return JsonResponse({"error": "Asset not found for the given token ID."}, status=404)

        # Ensure the sender owns the asset
        if asset.asset_owner != user:
            return JsonResponse({"error": "You do not own this asset."}, status=403)

        # Call the transfer_token function to interact with the blockchain
        result = transfer_token(int(token_id), to_address, account_id, private_key)

        # Update the asset owner
        print(f"Asset Owner Before Update: {asset.asset_owner}")
        asset.asset_owner = recipient_user
        asset.save()
        print(f"Asset Owner After Update: {asset.asset_owner}")

        # Update the user_address in the FileData model
        FileData.objects.filter(file_hash=asset.file_id).update(user_address=to_address)

        # Return success response
        return JsonResponse({
            "message": "Asset transferred successfully and FileData updated.",
            "updated_asset": {
                "asset_id": str(asset.asset_id),
                "new_owner": asset.asset_owner.username,
                "token_id": asset.token_id,
            },
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def recent_transactions_api(request):
    """
    API to fetch the most recent 5 transactions.
    """
    try:
        # Fetch the most recent 5 transactions
        transactions = TransactionData.objects.order_by('-time')[:10]

        # Serialize the transactions
        transactions_data = [
            {
                "transaction_id": str(transaction.transaction_id),
                "from_address": transaction.from_address,
                "to_address": transaction.to_address,
                "time": transaction.time.strftime("%Y-%m-%d %H:%M:%S"),
                "transaction_hash": transaction.transaction_hash,
                "block_number": transaction.block_number
            }
            for transaction in transactions
        ]

        # Return the serialized data
        return JsonResponse({"recent_transactions": transactions_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def all_transactions_api(request):
    """
    API to fetch all transactions involving the authenticated user.
    """
    try:
        # Get the authenticated user's public address
        user = request.user
        account_profile = AccountProfile.objects.get(user=user)
        user_public_address = account_profile.public_address

        # Fetch all transactions where the user is involved
        transactions = TransactionData.objects.filter(
            models.Q(from_address=user_public_address) |
            models.Q(to_address=user_public_address)
        ).order_by('-time')  # Order by most recent first

        # Serialize the transactions
        transactions_data = [
            {
                "transaction_id": str(transaction.transaction_id),
                "from_address": transaction.from_address,
                "to_address": transaction.to_address,
                "time": transaction.time.strftime("%Y-%m-%d %H:%M:%S"),
                "transaction_hash": transaction.transaction_hash,
                "block_number": transaction.block_number
            }
            for transaction in transactions
        ]

        # Return the serialized data
        return JsonResponse({"all_transactions": transactions_data}, status=200)

    except AccountProfile.DoesNotExist:
        return JsonResponse({"error": "Account profile not found for the user."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_metadata_upload_create_asset(request):
    """
    API to update metadata, upload file to IPFS, and create an asset.
    """
    data = request.data
    file_id = data.get("file_id")
    print(file_id)
    asset_name = data.get("name")

    if not file_id or not asset_name:
        return JsonResponse({"error": "File ID and asset name are required"}, status=400)

    try:
        # Check if the file_id already exists in an asset
        if AssetData.objects.filter(file_id__file_id=file_id).exists():
            return JsonResponse({"error": "An asset already exists for the provided file ID."}, status=400)

        # Get the authenticated user and their account profile
        user = request.user
        try:
            account_profile = AccountProfile.objects.get(user=user)
            public_address = account_profile.public_address
            private_key = account_profile.private_address
        except AccountProfile.DoesNotExist:
            return JsonResponse({"error": "Account profile not found for the user."}, status=404)

        # Retrieve the file data for the given file_id
        try:
            file_data = FileData.objects.get(file_id=file_id, user_address=public_address)
        except FileData.DoesNotExist:
            return JsonResponse({"error": "File not found for the given file ID."}, status=404)

        # Update metadata
        file_path_full = f"./media/{file_data.file_path}"
        new_hash_value = updateMetaData(file_path_full, file_path_full, public_address)
        file_data.file_hash_updated = new_hash_value
        file_data.save()

        # Upload file to IPFS
        ipfs_response = add_to_ipfs(file_path_full)
        ipfs_hash = ipfs_response.get("Hash")
        if not ipfs_hash:
            return JsonResponse({"error": "Failed to upload file to IPFS."}, status=500)
        file_data.ipfs_hash = ipfs_hash
        file_data.save()

        # Create the asset on the blockchain
        result = create_asset(ipfs_hash, asset_name, public_address, private_key)
        print(result)
        if not result:
            return JsonResponse({"error": "Failed to create asset on the blockchain."}, status=500)

        # Save the asset data to the database
        asset_data = AssetData.objects.create(
            block_number=result["block_number"],
            transaction_id=result["transaction_id"],
            token_id=result["token_id"],
            asset_owner=user,
            file_id=file_data,
            name=asset_name
        )

        print(asset_data)

        # Save the transaction data to the database
        TransactionData.objects.create(
            from_address=public_address,
            to_address=result["owner"],  # Assuming the blockchain returns the asset owner
            transaction_hash=result["transaction_id"],
            block_number=result["block_number"],
            created_by=user
        )

        # Return the response with asset details
        return JsonResponse({
            "message": "Metadata updated, file uploaded to IPFS, and asset created successfully.",
            "asset_id": str(asset_data.asset_id),
            "block_number": asset_data.block_number,
            "transaction_id": asset_data.transaction_id,
            "token_id": asset_data.token_id,
            "asset_owner": asset_data.asset_owner.username,
            "file_id": str(asset_data.file_id.file_id),
            "name": asset_data.name,
            "ipfs_hash": ipfs_hash,
            "created_at": asset_data.created_at
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_asset(request):
    file_id = request.GET.get('file_id')

    if not file_id:
        return Response({"error": "File ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if an asset exists for the given file ID
        asset = AssetData.objects.filter(file_id=file_id).first()

        if asset:
            return Response({"exists": True, "asset_hash": asset.token_id}, status=status.HTTP_200_OK)
        else:
            return Response({"exists": False}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_files_with_assets(request):
    try:
        user = request.user
        files = FileData.objects.filter(user_address=user.account_profile.public_address)

        response_data = []
        for file in files:
            asset = AssetData.objects.filter(file_id=file.file_id).first()
            response_data.append({
                "file_id": str(file.file_id),
                "file_metadata": file.file_metadata,
                "file_hash": file.file_hash,
                "ipfs_hash": file.ipfs_hash,
                "created_at": file.created_at,
                "updated_at": file.updated_at,
                "asset_id": str(asset.token_id) if asset else None,
            })

        return Response({"files": response_data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_user_asset_count(request):
    """
    API to get the count of assets owned by the authenticated user.
    """
    try:
        # Get the authenticated user
        user = request.user

        # Fetch and count the assets associated with the user
        asset_count = AssetData.objects.filter(asset_owner=user).count()

        # Return the count
        return Response({"total_assets": asset_count}, status=200)  # Updated response key to 'total_assets'
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_user_assets(request):
    """
    API to get the list and count of assets owned by the authenticated user.
    """
    try:
        # Get the authenticated user
        user = request.user

        # Fetch the assets associated with the user
        assets = AssetData.objects.filter(asset_owner=user)

        # Serialize the asset data
        serialized_assets = AssetDataSerializer(assets, many=True).data

        # Count the assets
        asset_count = assets.count()

        # Return the count and list
        return Response({
            "total_assets": asset_count,
            "assets": serialized_assets
        }, status=200)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
