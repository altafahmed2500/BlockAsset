from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileDataSerializer






@api_view(['POST'])
def fileUploadUpdateData(request):
    if request.method == 'POST':
        serializer = FileDataSerializer(data=request.data,request=request)

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
