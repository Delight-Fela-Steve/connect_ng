from rest_framework import serializers
from .models import Service, Booking, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']



class ServiceSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField()
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
        depth = 1


class ServiceListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.description}"

class BookingSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField()
    service = ServiceListingField(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'