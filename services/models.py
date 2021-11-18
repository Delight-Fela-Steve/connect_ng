from django.db import models
from django.conf import settings
# Create your models here.

class Service(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=56)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    starred = models.IntegerField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    pending = models.BooleanField(blank=True, null=True, default=True)
    accepted = models.BooleanField(blank=True, null=True)
    paid = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.service.name

