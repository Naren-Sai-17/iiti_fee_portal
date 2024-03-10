# django tools 
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.generic import ListView
# other files 
from .utils.upload import add_students
from .utils import verify
from . import forms
from . import models
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

class list(ListView): 
    model = models.Students
    template_name = "admin_portal/list.html"
    context_object_name = 'students_list'
    paginate_by = 100

def logs(request): 
    return render(request, "admin_portal/logs.html") 

@require_POST   
def upload_excel(request): 
    # no file found 
    if "student_upload_sheet" not in request.FILES:
        return redirect() 
    excel_file = request.FILES["student_upload_sheet"] 
    # wrong file type 
    if not verify.is_excel_file(excel_file): 
        return redirect(reverse("admin_portal:upload"))
    add_students(excel_file)
    # overview of additions 
    # show errors 
    # option to download excel of errors   
    return redirect(reverse("admin_portal:upload")) 