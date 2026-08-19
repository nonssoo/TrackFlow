from django.contrib import admin
from .models import Customer, Driver, Address, Shipment, ShipmentStatusHistory


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "phone_number")
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("__str__", "phone_number", "is_available")
    list_filter = ("is_available",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("street", "city", "state", "country")
    search_fields = ("street", "city", "postal_code")


class ShipmentStatusHistoryInline(admin.TabularInline):
    model = ShipmentStatusHistory
    extra = 0
    readonly_fields = ("status", "changed_at", "note")
    can_delete = False


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("tracking_number", "customer", "driver", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("tracking_number", "customer__user__username")
    inlines = [ShipmentStatusHistoryInline]