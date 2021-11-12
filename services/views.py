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
        print(services)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def service(request, id):
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def user_services(request, user_id):
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        service = Service.objects.filter(seller=user)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "PUT", "DELETE"])
def user_service(request, id, user_id):
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        service = Service.objects.get(pk=id, seller=user)
    except service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET", "PUT", "DELETE"])
def buyer_bookings(request, user_id):
    try:
        user = UserProfile.objects.get(pk=user_id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def buyer_booking(request, id, user_id):
    user = UserProfile.objects.get(pk=user_id)
    pass


def seller_bookings(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    pass


def seller_booking(request, id, user_id):
    user = UserProfile.objects.get(id=user_id)
    pass
