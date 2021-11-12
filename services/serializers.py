from rest_framework import serializers
from .models import Service, Booking

class ServiceSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = '__all__'
        


class BookingSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField()
    class Meta:
        model = Booking
        fields = '__all__'