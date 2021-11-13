from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import UserProfile
# drf_stuff
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

# Handles sign up
@csrf_exempt
@api_view(["POST"])
def register(request):
    if request.method == "POST":
        username = request.data["username"]
        email = request.data["email"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]

        # Ensure password matches confirmation
        password = request.data["password"]
        confirmation = request.data["confirmation"]
        if password != confirmation:
            return Response( {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create user profile at the same time
            user_profile = UserProfile.objects.create(user=user,first_name=first_name, last_name=last_name,)
            user_profile.save()
        except IntegrityError:
            return Response({
                "message": "Username already taken."
            }, status=status.HTTP_409_CONFLICT)
        login(request, user)
        return Response({"message":"Registered Successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


# Handles login
@csrf_exempt
@api_view(["POST"])
def sign_in(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return Response({"message":"Logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid username and/or password."
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

# Handles logout
@csrf_exempt
@api_view(["GET"])
def sign_out(request):
    logout(request)
    return Response({"message":"Logged out successfully"}, status=status.HTTP_200_OK)

