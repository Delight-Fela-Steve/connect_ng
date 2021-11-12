from django.urls import path
from . import views

urlpatterns=[
    path("services", views.services, name="services"),
    path("services/<int:id>", views.service, name="service"),
    path("user/<int:user_id>/services", views.user_services, name="user_services"),
    path("user/<int:user_id>/services/<int:id>", views.user_service, name="user_service"),
    path("user/<int:user_id>/buyer/bookings", views.buyer_bookings, name="buyer_bookings"),
    path("user/<int:user_id>/buyer/bookings/<int:id>", views.buyer_booking, name="buyer_booking"),
    path("user/<int:user_id>/seller/bookings", views.seller_bookings, name="seller_bookings"),
    path("user/<int:user_id>/seller/bookings/<int:id>", views.seller_booking, name="seller_booking"),
]