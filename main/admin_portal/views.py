from django.shortcuts import render

# Create your views here.
def index(request): 
    pass 

def base(request): 
    return render(request,"admin_portal/base.html")

def dashboard(request): 
    return render(request, "admin_portal/dashboard.html")