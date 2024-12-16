from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from UserAdmin.permisssion import IsAdminUser  # Assuming your custom permission is here
from .models import AccountProfile
from .serializers import AccountSerializer, UserNamePublicKeySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Allow only authenticated users to access this view
def get_user_names_and_public_keys(request):
    # Retrieve all account profiles excluding those linked to admin users
    account_profiles = AccountProfile.objects.filter(user__is_staff=False, user__is_superuser=False)

    # Serialize the data with the custom serializer
    serializer = UserNamePublicKeySerializer(account_profiles, many=True)

    return Response(serializer.data)


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
