from django.shortcuts import render
from .models import Service, Booking, Category
from .serializers import ServiceSerializer, BookingSerializer, CategorySerializer
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def category(request):
    if request.method == "GET":
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([AllowAny])
def services(request):
    if request.method == "GET":
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def service(request, id):
    try:
        service = Service.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book(request, id):
    try:
        user = User.objects.get(email=request.user.email)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        service = Service.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        # Confirm if the signed in user is not the owner of the service being checked
        if request.user.id !=  service.seller.id:
            booking, created = Booking.objects.get_or_create(buyer=user, service=service)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"You cannot book your own service",}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated,))
def user_services(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    # Confirm if the signed in user is the owner of the service being checked
    if request.user.id !=  user.id:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        service = Service.objects.filter(seller=user)
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        service = Service(seller=user)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            service = Service.objects.get(id=serializer.data["id"])
            for category in request.data["category"]:
                name = Category.objects.get(name=category["name"])
                print(type(name))
                service.category.add(name)
            serializer_modified = ServiceSerializer(service)
            return Response(serializer_modified.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_service(request, id, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        service = Service.objects.get(pk=id, seller=user)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the service being checked
    print(request.user.id)
    if request.user.id !=  service.seller.id:
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
@permission_classes([IsAuthenticated])
def seller_bookings(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the bookings being checked
    if request.user.id !=  user.id:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        bookings = Booking.objects.filter(service__seller=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
        

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def seller_booking(request, id, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Confirm if the signed in user is the owner of the booking being checked
    if request.user.id !=  user.id:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(pk=id, service__seller=user)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

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
@permission_classes([IsAuthenticated])
def buyer_bookings(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
    print(request.user.id, user.id)
    # Confirm if the signed in user is the owner of the bookings being checked
    if request.user.id !=  user.id:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        bookings = Booking.objects.filter(buyer=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def buyer_booking(request, id, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    # Confirm if the signed in user is the owner of the booking being checked
    if request.user.id !=  user.id:
        return Response({"message":"Invalid User"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        booking = Booking.objects.get(pk=id, buyer=user)
    except ObjectDoesNotExist:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

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
    
