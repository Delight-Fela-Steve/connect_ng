from rest_framework import serializers
from .models import Service, Booking

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking