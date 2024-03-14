from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as dj_logout
from allauth.account.views import LogoutView 
from .decorators import is_student

# Create your views here.
def index(request): 
    if request.user.is_authenticated: 
        return redirect(reverse("student_portal:dashboard"))
    return render(request, "login.html")

@is_student
def dashboard(request): 
    return render(request, "dashboard.html")

def logout(request): 
    dj_logout(request) 
    return redirect(reverse("student_portal:login"))

def not_authorized(request): 
    return render(request,"not_authorized.html")