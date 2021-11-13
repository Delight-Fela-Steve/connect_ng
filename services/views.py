from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authenticate.models import UserProfile
from .models import Service, Booking
from .serializers import ServiceSerializer, BookingSerializer


# Create your views here.
@api_view(["GET"])
def services(request):
    if request.method == "GET":
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def service(request, id):
    try:
        service = Service.objects.get(pk=id)
    except service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


@api_view(["POST"])
def book(request, user_id, id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is not the owner of the service being checked
    if request.user.username !=  user.user.username:
        try:
            service = Service.objects.get(pk=id)
        except service.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        booking = Booking.objects.create(buyer=user, service=service)
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET", "POST"])
def user_services(request, user_id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the service being checked
    if request.user.username !=  user.user.username:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        service = Service.objects.filter(seller=user)
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT", "DELETE"])
def user_service(request, id, user_id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        service = Service.objects.get(pk=id, seller=user)
    except service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the service being checked
    if request.user.username !=  service.seller.user.username:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
def seller_bookings(request, user_id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the bookings being checked
    if request.user.username !=  user.user.username:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        bookings = Booking.objects.filter(service__seller=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
        

@api_view(["GET", "PUT", "DELETE"])
def seller_booking(request, id, user_id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Confirm if the signed in user is the owner of the booking being checked
    if request.user.username !=  user.user.username:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(pk=id, service__seller=user)
    except booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET"])
def buyer_bookings(request, user_id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the bookings being checked
    if request.user.username !=  user.user.username:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        bookings = Booking.objects.filter(service__seller=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

@api_view(["GET", "PUT", "DELETE"])
def buyer_booking(request, id, user_id):
    if not request.user.is_authenticated:
        return Response({"message":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the booking being checked
    if request.user.username !=  user.user.username:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(pk=id, buyer=user)
    except booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
