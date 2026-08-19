from django.shortcuts import render, redirect
from .models import Shipment, DeliveryRequest, ShipmentStatusHistory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import random
import string
from django.contrib import messages




def track_shipment(request):
    shipment = None
    error = None
    tracking_number = request.GET.get("tracking_number")

    if tracking_number:
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
        except Shipment.DoesNotExist:
            error = f"No shipment found with tracking number '{tracking_number}'."

    return render(request, "shipments/track.html", {
        "shipment": shipment,
        "error": error,
        "tracking_number": tracking_number,
    })
    
    
@login_required
def customer_dashboard(request):
    customer = request.user.customer_profile
    shipments = customer.shipments.all()

    return render(request, "shipments/dashboard.html", {
        "shipments": shipments,
    })
    
    
@login_required
def shipment_detail(request, pk):
    customer = request.user.customer_profile
    shipment = get_object_or_404(Shipment, pk=pk, customer=customer)

    return render(request, "shipments/detail.html", {"shipment": shipment})

from .forms import DeliveryRequestForm


@login_required
def create_delivery_request(request):
    customer = request.user.customer_profile

    if request.method == "POST":
        form = DeliveryRequestForm(request.POST)
        if form.is_valid():
            form.save(customer=customer)
            messages.success(request, "Your delivery request has been submitted. Staff will review it shortly.")
            return redirect("customer_dashboard")
    else:
        form = DeliveryRequestForm()

    return render(request, "shipments/request_form.html", {"form": form})

@staff_member_required
def staff_dashboard(request):
    pending_requests = DeliveryRequest.objects.filter(status="submitted")
    all_shipments = Shipment.objects.all().order_by("-created_at")

    return render(request, "shipments/staff_dashboard.html", {
        "pending_requests": pending_requests,
        "all_shipments": all_shipments,
    })
    
    
def generate_tracking_number():
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"TF-{suffix}"


    
    
@staff_member_required
def approve_request(request, pk):
    delivery_request = get_object_or_404(DeliveryRequest, pk=pk)

    if delivery_request.status != "submitted":
        return redirect("staff_dashboard")

    if request.method == "POST":
        shipment = Shipment.objects.create(
            tracking_number=generate_tracking_number(),
            customer=delivery_request.customer,
            origin=delivery_request.pickup_address,
            destination=delivery_request.destination_address,
            weight_kg=delivery_request.weight_kg,
            status="pending",
        )
        ShipmentStatusHistory.objects.create(
            shipment=shipment, status="pending", note="Shipment created from approved request."
        )
        delivery_request.status = "approved"
        delivery_request.shipment = shipment
        delivery_request.save()
        return redirect("staff_dashboard")

    return render(request, "shipments/approve_request.html", {"delivery_request": delivery_request})

@login_required
def customer_dashboard(request):
    if not hasattr(request.user, "customer_profile"):
        return redirect("home")

    customer = request.user.customer_profile
    shipments = customer.shipments.all()
    pending_requests = customer.delivery_requests.filter(status="submitted")

    return render(request, "shipments/dashboard.html", {
        "shipments": shipments,
        "pending_requests": pending_requests,
    })
    
@login_required
def cancel_delivery_request(request, pk):
    customer = request.user.customer_profile
    delivery_request = get_object_or_404(
        DeliveryRequest, pk=pk, customer=customer, status="submitted"
    )

    if request.method == "POST":
        delivery_request.delete()
        messages.success(request, "Your delivery request has been cancelled.")
        return redirect("customer_dashboard")

    return render(request, "shipments/cancel_request.html", {"delivery_request": delivery_request})

@staff_member_required
def reject_request(request, pk):
    delivery_request = get_object_or_404(DeliveryRequest, pk=pk, status="submitted")

    if request.method == "POST":
        delivery_request.status = "rejected"
        delivery_request.save()
        messages.success(request, f"Request from {delivery_request.customer} has been rejected.")
        return redirect("staff_dashboard")

    return render(request, "shipments/reject_request.html", {"delivery_request": delivery_request})