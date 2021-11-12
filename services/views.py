from django.shortcuts import render
from authenticate.models import UserProfile
from .models import Service, Booking


# Create your views here.

def services(request):
    if request.method == "POST":

    if request.method == "GET":
        services == Service.objects.all()
        pass


def service(request, id):
    if request.method == "GET":
        service == Service.objects.get(id==id)
        pass


def user_services(request, user_id):
    user == UserProfile.objects.get(id==user_id)
    if request.method == "GET":
        service == Service.objects.filter(seller == user)
        pass


def user_service(request, id, user_id):
    user == UserProfile.objects.get(id==user_id)
    pass


def buyer_bookings(request, user_id):
    user == UserProfile.objects.get(id==user_id)
    pass


def buyer_booking(request, id, user_id):
    user == UserProfile.objects.get(id==user_id)
    pass


def seller_bookings(request, user_id):
    user == UserProfile.objects.get(id==user_id)
    pass


def seller_booking(request, id, user_id):
    user == UserProfile.objects.get(id==user_id)
    pass
