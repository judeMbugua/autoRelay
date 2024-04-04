from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def signIn(request):
    context = {"error":'none'}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            context['error'] = "There was a log in error,please try again"
            return redirect("login")

    else:
        return render(request, "accounts/login.html")


def log_out(request):
    logout(request)
    return render(request, "accounts/logout.html")
