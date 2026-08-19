from django.db import models
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Driver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_profile"
    )
    phone_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}"


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Pickup"),
        ("picked_up", "Picked Up"),
        ("at_hub", "Arrived at Hub"),
        ("in_transit", "In Transit"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivery_attempted", "Delivery Attempted"),
        ("delivered", "Delivered"),
        ("delayed", "Delayed"),
        ("cancelled", "Cancelled"),
    ]
        
    
                

    tracking_number = models.CharField(max_length=20, unique=True)
    
    
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="shipments"
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="shipments"
    )
    origin = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="origin_shipments"
    )
    destination = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="destination_shipments"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_number} ({self.get_status_display()})"


class ShipmentStatusHistory(models.Model):
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="status_history"
    )
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.shipment.tracking_number} -> {self.status} at {self.changed_at}"
    
    
class DeliveryRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="delivery_requests"
    )
    pickup_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="pickup_requests"
    )
    destination_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="destination_requests"
    )
    package_description = models.CharField(max_length=255)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=REQUEST_STATUS_CHOICES, default="submitted"
    )
    shipment = models.OneToOneField(
        Shipment, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="originating_request"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.customer} — {self.get_status_display()}"