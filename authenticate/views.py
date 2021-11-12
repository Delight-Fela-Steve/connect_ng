from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import UserProfile

# Create your views here.

# Handles sign up
@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return JsonResponse( {
                "message": "Passwords must match."
            }, safe=False)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create user profile at the same time
            user_profile = UserProfile.objects.create(user=user,first_name=first_name, last_name=last_name,)
            user_profile.save()
        except IntegrityError:
            return JsonResponse({
                "message": "Username already taken."
            }, safe=False)
        login(request, user)
        return JsonResponse({"message":"Registered Successfully"}, safe=False)
    else:
        return JsonResponse({"message":"Bad Request"}, safe=False)


# Handles login
@csrf_exempt
def sign_in(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({"message":"Logged in successfully"}, safe=False)
        else:
            return JsonResponse({
                "message": "Invalid username and/or password."
            }, safe=False)
    else:
        return JsonResponse({"message":"Bad Request"}, safe=False)

# Handles logout
@csrf_exempt
def sign_out(request):
    logout(request)
    return JsonResponse({"message":"Logged out successfully"}, safe=False)

