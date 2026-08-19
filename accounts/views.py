from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from shipments.models import Customer


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})