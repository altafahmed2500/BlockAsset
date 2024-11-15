from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from UserAdmin.permisssion import IsAdminUser  # Assuming your custom permission is here
from .models import AccountProfile
from .serializers import AccountSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])  # Restrict to admin users
def get_all_users(request):
    # Retrieve all user profiles from the database
    account_profiles = AccountProfile.objects.all()
    # Serialize the user profiles
    serializer = AccountSerializer(account_profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_account(request):
    # Retrieve the account details for the authenticated user
    try:
        account = AccountProfile.objects.get(user=request.user)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except AccountProfile.DoesNotExist:
        return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
