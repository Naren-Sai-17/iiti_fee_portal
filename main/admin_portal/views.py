# django tools 
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
# other files 
from .add_students import upload_and_save
from . import forms
# 3rd party tools 
import openpyxl

def login(request): 
    if request.method == "POST": 
        form = forms.LoginForm(request.POST) 
        if form.is_valid(): 
            return redirect(reverse("admin_portal:dashboard"))
    else: 
        form = forms.LoginForm() 
    context = {
        "form" : form
    }
    return render(request,"admin_portal/login.html",context)

def base(request): 
    return render(request,"admin_portal/base.html")

def dashboard(request): 
    
    return render(request, "admin_portal/dashboard.html")

def upload(request): 
    context = {
        "excel_form" : forms.StudentSheetUploadForm , 
    }
    return render(request, "admin_portal/upload.html",context)

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
    workbook = openpyxl.load_workbook(excel_file) 
    sheet = workbook.active
    for row in sheet.iter_rows(min_row =3 , max_row = 10, min_col = 2, max_col = 6, values_only = True):
        print(row) 
    return redirect(reverse("admin_portal:upload")) 