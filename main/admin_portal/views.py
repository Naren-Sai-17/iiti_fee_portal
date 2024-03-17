# django tools 
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .utils.upload import add_students
from django.views.generic import ListView
from . import forms
from . import models
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .filters import studentfilter
# 3rd party tools 
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

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset=studentfilter(self.request.GET,queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=self.filterset
        return context

    # to apply is_admin decorator to the class 
    @method_decorator(is_admin)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    import hashlib
import re


@is_admin
def profile(request, roll_number): 
    try:
        student_details = models.Students.objects.get(roll_number=roll_number)
        return render(request, 'admin_portal/profile.html', {
            'student_details': student_details,
        })
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return HttpResponse(error_message)

# @is_admin
# def profile(request,roll_number):
#     print("here")
#     try:
#         student_details = models.Students.objects.get(roll_number=roll_number)
#         print("here")
#         return render(request, 'admin_portal/profile.html', {
#             'student_details': student_details,
#         })
#     except Exception as e:
#         error_message = f"An error occurred: {str(e)}"
#         print(error_message)
#         return HttpResponse(error_message)

# Function to get the Gravatar image URL based on the email address
def get_gravatar_url(email):
    hash_value = hashlib.md5(email.lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?d=identicon&s=200"

    


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