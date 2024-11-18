from datetime import time

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FileData
from .serializers import FileDataSerializer
from AccountAdmin.models import AccountProfile
from .updateMetaData import updateMetaData, generate_file_hash
from .IPFSConnect import add_to_ipfs


@api_view(['GET'])
def getUserUploadFiles(request):
    account = AccountProfile.objects.get(user=request.user)
    user_address = account.public_address
    # Get the file data related to the user address
    file_data = FileData.objects.filter(user_address=user_address)
    # If no file data is found
    if not file_data.exists():
        return Response({"message": "No file data found for this user."}, status=status.HTTP_404_NOT_FOUND)
    # Serialize the data (replace FileDataSerializer with your actual serializer class)
    serializer = FileDataSerializer(file_data, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def updateMetadata(request):
    try:
        # Get the public address from the AccountProfile of the current user
        account = AccountProfile.objects.get(user=request.user)
        public_address = account.public_address

        # Retrieve the FileData object related to the user address
        file_data = FileData.objects.filter(user_address=public_address).first()

        # If no file data is found
        if not file_data:
            return Response({"message": "No file data found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Get the file path and file ID
        file_id = file_data.file_id
        file_path = file_data.file_path

        # Call updateMetaData with the retrieved file path and public address
        file_path_full = f"./media/{file_path}"
        new_hash_value = updateMetaData(file_path_full, file_path_full, public_address)

        # Update the metadata or hash in the database (if needed)
        # new_hash_value = generate_file_hash(file_path_full, hash_algorithm='sha256')
        # Replace with actual logic for new hash
        file_data.file_hash_updated = new_hash_value
        file_data.save()

        return Response(
            {"message": f"Metadata updated successfully for file_id: {file_id}"},
            status=status.HTTP_200_OK
        )

    except AccountProfile.DoesNotExist:
        return Response({"message": "Account not found for the user."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def fileUploadUpdateData(request):
    if request.method == 'POST':
        serializer = FileDataSerializer(data=request.data, request=request)

        # Validate the incoming data
        if serializer.is_valid():
            # Save the file and automatically generate metadata
            file_data = serializer.save()

            # Get the file path from the saved instance
            file_path = file_data.file_path.url  # This will give the media URL path

            # Construct the full metadata response
            response_data = {
                'file_id': file_data.file_id,
                'file_metadata': file_data.file_metadata,  # Auto-generated metadata
                'file_hash': file_data.file_hash,
                'file_path': request.build_absolute_uri(file_path),  # Full URL to the file
                'created_at': file_data.created_at,
                'updated_at': file_data.updated_at,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def uploadFileIPFS(request):
    try:
        # Get the public address from the AccountProfile of the current user
        account = AccountProfile.objects.get(user=request.user)
        public_address = account.public_address
        file_data = FileData.objects.filter(user_address=public_address).first()

        if not file_data:
            return Response({"message": "No file data found for this user."}, status=status.HTTP_404_NOT_FOUND)

        file_id = file_data.file_id
        file_path = file_data.file_path
        file_path_full = f"./media/{file_path}"

        ipfs_json = add_to_ipfs(file_path_full)
        ipfs_hash = ipfs_json["Hash"]
        file_data.ipfs_hash = ipfs_hash
        file_data.save()

        return Response(
            {"message": f"The file with ID{file_id} is uploaded to IPFS Distributed network and the details: {ipfs_json}"},
            status=status.HTTP_200_OK
        )
    except AccountProfile.DoesNotExist:
        return Response({"message": "Account not found for the user."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

