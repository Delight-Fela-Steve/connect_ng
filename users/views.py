from .models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.db import IntegrityError
# drf_stuff
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

# Create your views here.

# Handles sign up
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    if request.method == "POST":
        email = request.data["email"]
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        password = request.data["password"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return Response({
                "message": "email already taken."
            }, status=status.HTTP_409_CONFLICT)
        login(request, user)
        serializer = UserSerializer(user)
        token=Token.objects.get(user=user)
        key=token.key
        return Response({"message":"Registered Successfully","data":serializer.data, "token":key}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


# Handles login
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.data["email"]
        password = request.data["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            try:
                token=Token.objects.get(user=user)
                key=token.key
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response({"message":"Logged in successfully","data":serializer.data, "token":key}, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid email and/or password."
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

# Handles logout
@api_view(["GET"])
@permission_classes([AllowAny])
def sign_out(request):
    logout(request)
    return Response({"message":"Logged out successfully"}, status=status.HTTP_200_OK)

