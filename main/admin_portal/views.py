from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from . import utils
from django.views.generic import ListView
from . import forms
from . import models
from django.forms.models import model_to_dict
from django.http import QueryDict
from django.views import View
from django.conf import settings

import os 
from .filters import studentfilter
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from .decorators import is_admin
from django.contrib import messages


########## Dashboard ##########
@is_admin
def dashboard(request):
    return render(request, "admin_portal/dashboard.html")


@is_admin
def activate(request):
    for student in models.Students.objects.all(): 
        student.activate() 
    messages.success(request,"activated succesfully")
    utils.log("fee portal activated")
    return redirect(reverse("admin_portal:dashboard"))


########## Add Students ##########
@is_admin
def upload(request):
    if request.method == "GET":
        return render(request, "admin_portal/upload.html")
    else:
        try:
            if models.Students.objects.filter(
                roll_number=request.POST["roll_number"]
            ).exists():
                raise Exception("Student already exists")
            student = models.Students()
            student.name = request.POST["name"]
            student.roll_number = request.POST["roll_number"]
            student.course = request.POST["course"]
            student.category = request.POST["category"]
            student.department = request.POST["department"]
            utils.calculate_fee_structure(student)
            messages.success(request, "Student added succesfully")
            utils.log(f"student {student.roll_number} added")
            return redirect(reverse("admin_portal:upload"))

        except Exception as e:
            messages.error(request, str(e))
            return redirect(reverse("admin_portal:upload"))


########## Delete Students ##########
@is_admin
def delete_student(request, roll_number):
    try:
        student = models.Students.objects.get(roll_number=roll_number)
        student.delete()
        utils.log(f"student {roll_number} deleted")
        messages.success(request, "student deleted succesfully")
        return redirect(reverse("admin_portal:list"))
    except Exception as e:
        print(e) 
        messages.error(request, e)
        return redirect(reverse("admin_portal:list"))

@is_admin 
def delete(request): 
    if request.method == "POST":  
            try:
                excel_file = request.FILES["excel_file"]
                utils.delete_student(excel_file)
                messages.success(request, "deleted students succesfully")
            except Exception as e:
                messages.error(request, f"error: {e}")
    else: 
        return render(request,"admin_portal/delete.html")
########## Fee Remission ##########
@is_admin
def remission(request):
    if request.method == "POST":
        try:
            roll_number = request.POST["roll_number"]
            remission_percentage = request.POST["remission_percentage"]
            utils.set_remission(roll_number, int(remission_percentage))
            messages.success(request, "database updated succesfully")
        except Exception as e:
            print(e)
            messages.error(request, e)
        return redirect(reverse("admin_portal:remission"))
    else:
        queryset = models.FeeRemission.objects.all()
        return render(
            request, "admin_portal/remission.html", {"remission_list": queryset}
        )


@is_admin
def clear_remission(request):
    try:
        for remission_instance in models.FeeRemission.objects.all():
            utils.delete_remission(remission_instance)
        messages.success(request, "database cleared succesfully")
    except:
        messages.error(request, "Error")
    return redirect(reverse("admin_portal:remission"))


@is_admin
def delete_remission(request, id):
    try:
        student_instance = models.Students.objects.get(roll_number=id)
        remission_instance = student_instance.remission
        utils.delete_remission(remission_instance)
        messages.success(request, "deleted succesfully")
    except Exception as e:
        messages.error(request, e)
    return redirect(reverse("admin_portal:remission"))


@is_admin
@require_POST
def group_remission(request):
    try:
        excel_file = request.FILES["excel_file"]
        utils.excel_remission(excel_file)
        messages.success(request, "database updated succesfully")
    except Exception as e:
        messages.error(request, f"error: {e}")
    return redirect(reverse("admin_portal:remission"))


########## Student List ##########
class list(ListView):
    model = models.Students
    template_name = "admin_portal/list.html"
    context_object_name = "students_list"
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = studentfilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset

        # Retain filter parameters in pagination links
        querydict = QueryDict(mutable=True)
        querydict.update(self.request.GET)
        context["querydict"] = querydict.urlencode()

        return context

    @method_decorator(is_admin)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


########## Fee Structure ##########
@is_admin
def fee_structure_list(request):
    fee_structures = models.FeeStructure.objects.all()
    if request.method == "POST":
        fee_structure_id = request.POST.get("fee_structure_id")
        try:
            fee_structure_instance = models.FeeStructure.objects.get(
                id=fee_structure_id
            )
            form = forms.FeeStructureForm(request.POST, instance=fee_structure_instance)
            if form.is_valid():
                fee_structure_instance = form.save()
                update_count = utils.recalculate_fee_structure(fee_structure_instance)
                messages.success(
                    request, f"fee structure of {update_count} updated successfully"
                )
                return redirect(reverse("admin_portal:structure"))
            else:
                return redirect(reverse("admin_portal:structure"))
        except Exception as e:
            form = forms.FeeStructureForm(request.POST, auto_id=True)
            try:
                fee_structure_instance = form.save()
                messages.success(request, "fee structure added succesfully")
                update_count = utils.recalculate_fee_structure(fee_structure_instance)
                messages.success(
                    request, f"fee structure of {update_count} updated successfully"
                )
                return redirect(reverse("admin_portal:structure"))
            except:
                messages.error(request, "incorrect formatting")
                return redirect(reverse("admin_portal:structure"))
    else:
        return render(
            request, "admin_portal/structure.html", {"fee_structures": fee_structures}
        )


########## Student Profile ##########
@is_admin
def profile(request, roll_number):
    try:
        student_details = models.Students.objects.get(roll_number=roll_number)
        return render(
            request,
            "admin_portal/profile.html",
            {
                "student_details": student_details,
            },
        )
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return HttpResponse(error_message)


@is_admin
@require_POST
def update_profile(request):
    roll_number = request.POST["roll_number"]
    student = models.Students.objects.get(roll_number=roll_number)
    form = forms.Profile(request.POST, instance=student)
    print(form)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        messages.success(request, "fee updated succesfully")
        return redirect(reverse("admin_portal:profile", args=[roll_number]))
    else:
        messages.error(request, "invalid input")
        return redirect(reverse("admin_portal:profile", args=[roll_number]))

########## Download Excel ##########
def download_excel(request, id):
    id += ".xlsx"
    excel_file_path = os.path.join(settings.BASE_DIR, 'static', 'excel', id)    
    try:
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')        
            response['Content-Disposition'] = f'attachment; filename="{id}"'
            return response
    except FileNotFoundError:
        print("File not found:", excel_file_path)
        return HttpResponse("File not found.", status=404)
    except Exception as e:
        print("An error occurred:", e)
        return HttpResponse("An error occurred.", status=500)
    
########## Admin logs ##########
@is_admin
def logs(request):
    logs = models.Log.objects.all().order_by('-timestamp')
    return render(request, 'admin_portal/logs.html', {'logs': logs})

@require_POST
@is_admin
def upload_excel(request):
    excel_file = request.FILES["excel_file"]
    utils.add_students(excel_file)
    return redirect(reverse("admin_portal:upload"))


########## Authentication ##########
def login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user)
                return redirect(reverse("admin_portal:dashboard"))
    else:
        form = forms.LoginForm()
    return render(request, "admin_portal/login.html", {"form": form})


def logout(request):
    dj_logout(request)
    return redirect(reverse("admin_portal:login"))


def not_authorized(request):
    return render(request, "admin_portal/not_authorized.html")
