from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import UserProfileSerializer
from .models import UserProfile, Incident
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .permisssion import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .verify_location import get_location_from_ip, get_client_ip, ALLOWED_COUNTRIES


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World!"})


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_profile(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_user_profiles(request):
    # Retrieve all user profiles from the database
    user_profiles = UserProfile.objects.all()

    # Serialize the user profiles
    serializer = UserProfileSerializer(user_profiles, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def secure_view(request):
    return Response({'message': 'You are authenticated!'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Verify_user(request):
    ip = get_client_ip(request)
    location_data = get_location_from_ip(ip)

    if not location_data:
        return Response({"error": "Could not fetch location info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    country = location_data.get("country")
    city = location_data.get("city")

    if country in ALLOWED_COUNTRIES:
        return Response({
            "status": "verified",
            "country": country,
            "city": city,
            "ip": ip
        })
    else:
        return Response({
            "status": "denied",
            "country": country,
            "city": city,
            "ip": ip
        }, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def login_view(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password."}, status=HTTP_400_BAD_REQUEST)


def logout_view(request):
    logout(request)
    return redirect('login')


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def create_incident(request):
    """
    API endpoint to create a new incident for the authenticated user.
    """
    user = request.user
    incident_name = request.data.get('incident_name')
    incident_description = request.data.get('incident_description', '')

    if not incident_name:
        return Response({"error": "Incident name is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create a new incident for the authenticated user
        incident = Incident.objects.create(
            user=user,
            incident_name=incident_name,
            incident_description=incident_description
        )
        return Response({
            "message": "Incident created successfully.",
            "incident": {
                "incident_id": incident.incident_id,
                "incident_name": incident.incident_name,
                "incident_description": incident.incident_description,
                "created_at": incident.created_at,
                "updated_at": incident.updated_at
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)