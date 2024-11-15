from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .permisssion import IsAdminUser


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to a success page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('login')
