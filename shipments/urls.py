from django.urls import path
from . import views

urlpatterns = [
    path("track/", views.track_shipment, name="track_shipment"),
    path("dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("shipment/<int:pk>/", views.shipment_detail, name="shipment_detail"),
    path("request/", views.create_delivery_request, name="create_delivery_request"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/approve/<int:pk>/", views.approve_request, name="approve_request"),
    path("request/<int:pk>/cancel/", views.cancel_delivery_request, name="cancel_delivery_request"),
    path("staff/reject/<int:pk>/", views.reject_request, name="reject_request"),

]