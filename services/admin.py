from django.contrib import admin
from .models import Service, Booking, Category
# Register your models here.
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Category)
