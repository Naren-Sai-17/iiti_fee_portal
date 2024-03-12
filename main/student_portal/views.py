from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout as django_logout
from allauth.account.views import LogoutView 

# Create your views here.
def index(request): 
    if request.user.is_authenticated: 
        return HttpResponseRedirect(reverse("student_portal:dashboard"))
    return render(request, "login.html")
def dashboard(request): 
    return render(request, "dashboard.html")

