from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
    
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .permisssion import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken


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


@permission_classes([IsAdminUser])
@api_view(['GET'])
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
