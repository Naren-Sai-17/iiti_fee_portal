from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import LoginForm
from django.http import HttpResponse
# Create your views here.

def login(request): 
    if request.method == "POST": 
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            return redirect(reverse("admin_portal:dashboard"))
    else: 
        form = LoginForm() 
    
    return render(request,"admin_portal/login.html",{"form": form})

def base(request): 
    return render(request,"admin_portal/base.html")

def dashboard(request): 
    return render(request, "admin_portal/dashboard.html")

def upload(request): 
    return render(request, "admin_portal/upload.html")

def list(request): 
    return render(request, "admin_portal/list.html") 

def logs(request): 
    return render(request, "admin_portal/logs.html") 