# django tools 
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
# other files 
from .add_students import upload_and_save
from . import forms
# 3rd party tools 

def login(request): 
    if request.method == "POST": 
        form = forms.LoginForm(request.POST) 
        if form.is_valid(): 
            return redirect(reverse("admin_portal:dashboard"))
    else: 
        form = forms.LoginForm() 
    
    return render(request,"admin_portal/login.html",{"form": form})

def base(request): 
    return render(request,"admin_portal/base.html")

def dashboard(request): 
    return render(request, "admin_portal/dashboard.html")

def upload(request): 
    return render(request, "admin_portal/upload.html",{"excel_form" : forms.StudentUploadForm})

def list(request): 
    return render(request, "admin_portal/list.html") 

def logs(request): 
    return render(request, "admin_portal/logs.html") 

@require_POST   
def upload_excel(request): 
    excel_file = request.FILES["student_upload_sheet"] 
    upload_and_save(excel_file)
    ### check recieved data 
    ### handle excel file 
    return redirect(reverse("admin_portal:upload")) 