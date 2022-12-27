from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, Patient, Appointment

# Create your views here.


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist")
            return redirect("login")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password does not exist")

    context = {}
    return render(request, "base/loginregister.html", context)


def homepage(request):
    context = {}
    return render(request, "base/home.html", context)


def aboutpage(request):
    context = {}
    return render(request, "base/about.html", context)


def contactpage(request):
    context = {}
    return render(request, "base/contact.html", context)
