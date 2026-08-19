from django import forms
from .models import DeliveryRequest, Address


class DeliveryRequestForm(forms.ModelForm):
    pickup_street = forms.CharField(max_length=255, label="Pickup street address")
    pickup_city = forms.CharField(max_length=100, label="Pickup city")
    destination_street = forms.CharField(max_length=255, label="Destination street address")
    destination_city = forms.CharField(max_length=100, label="Destination city")

    class Meta:
        model = DeliveryRequest
        fields = ["package_description", "weight_kg"]

    def save(self, customer, commit=True):
        pickup = Address.objects.create(
            street=self.cleaned_data["pickup_street"],
            city=self.cleaned_data["pickup_city"],
            state="", postal_code="", country=""
        )
        destination = Address.objects.create(
            street=self.cleaned_data["destination_street"],
            city=self.cleaned_data["destination_city"],
            state="", postal_code="", country=""
        )
        request_obj = super().save(commit=False)
        request_obj.customer = customer
        request_obj.pickup_address = pickup
        request_obj.destination_address = destination
        if commit:
            request_obj.save()
        return request_obj