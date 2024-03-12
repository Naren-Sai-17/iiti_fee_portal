# django tools 
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .utils.upload import add_students
from django.views.generic import ListView
from . import forms
from . import models
from django.utils.decorators import method_decorator
from .decorators import is_admin
from django.contrib.auth import logout

def login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
                return redirect(reverse("admin_portal:dashboard"))
    else:
        form = forms.LoginForm()
    return render(request, "admin_portal/login.html", {"form": form})


def base(request): 
    return render(request,"admin_portal/base.html")

@is_admin
def dashboard(request): 
    return render(request, "admin_portal/dashboard.html")

@is_admin
def upload(request): 
    return render(request, "admin_portal/upload.html",{"excel_form" : forms.StudentUploadForm})

class list(ListView): 
    model = models.Students
    template_name = "admin_portal/list.html"
    context_object_name = 'students_list'
    paginate_by = 100

    # to apply is_admin decorator to the class 
    @method_decorator(is_admin)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@is_admin
def logs(request): 
    return render(request, "admin_portal/logs.html") 

@require_POST  
@is_admin
def upload_excel(request): 
    # no file found 
    # if "student_upload_sheet" not in request.FILES:
    #     return redirect() 
    excel_file = request.FILES["excel_file"] 
    # wrong file type 
    # if not verify.is_excel_file(excel_file): 
        # return redirect(reverse("admin_portal:upload"))
    add_students(excel_file)
    # overview of additions 
    # show errors 
    # option to download excel of errors   
    return redirect(reverse("admin_portal:upload")) 

def logout(request): 
    dj_logout(request) 
    return redirect(reverse("admin_portal:login"))

def not_authorized(request): 
    return render(request, "admin_portal/not_authorized.html") 