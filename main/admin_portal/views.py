import pandas as pd
from .models import Students
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from . import utils
from django.views.generic import ListView
from . import forms
from . import models
from django.db.models import Q
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

def reconciliation(request): 
    print("here")
    save_path = utils.reconciliation()
    with open(save_path, "rb") as excel_file:
        response = HttpResponse(
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="reconciliation.xlsx"'
    return response


# dummy function for testing purpose 
def make_payment(request):
    if request.method == "GET": 
        return render(request,'admin_portal/make_payment.html') 
    else: 
        roll_number = request.POST['roll_number']
        amount = request.POST['amount'] 
        student = models.Students.objects.get(roll_number = roll_number) 
        student.make_payment(amt=amount) 
        return redirect(reverse('admin_portal:profile',args = [roll_number]))

def loan(request): 
    if request.method == "GET": 
        return render(request,'admin_portal/loan.html')
    else: 
        excel_file = request.FILES["excel_file"]
        utils.loan_excel(excel_file)
        utils.log("Added loan payments")
        messages.success(request, "database updated succesfully")
        return redirect(reverse('admin_portal:loan'))

########## Dashboard ##########
@is_admin
def dashboard(request):

    btech_students = Students.objects.filter(course__icontains='B.TECH').count()
    mtech_students = Students.objects.filter(course__icontains='M.TECH').count()
    msc_students = Students.objects.filter(course__icontains='MSC').count()
    phd_students = Students.objects.filter(course__icontains='PHD').count()
    all_students = Students.objects.all().count()
    btech_no_due = Students.objects.filter(course__icontains='B.TECH', fee_payable__lte=0).count()
    mtech_no_due = Students.objects.filter(course__icontains='M.TECH', fee_payable__lte=0).count()
    msc_no_due = Students.objects.filter(course__icontains='MSC', fee_payable__lte=0).count()
    phd_no_due = Students.objects.filter(course__icontains='PHD', fee_payable__lte=0).count()
    all_no_due = Students.objects.filter(fee_payable__lte=0).count()
    semester = models.Variable.objects.get(name = "semester")
    context = {
        'all_students': all_students,
        'btech_students': btech_students,
        'mtech_students': mtech_students,
        'msc_students': msc_students,
        'phd_students': phd_students,
        'all_no_due': all_no_due, 
        'btech_no_due': btech_no_due, 
        'mtech_no_due': mtech_no_due, 
        'msc_no_due': msc_no_due, 
        'phd_no_due': phd_no_due, 
        'semester' : semester.value
    }

    return render(request, "admin_portal/dashboard.html", context=context)

def set_semester(request): 
    semester = models.Variable.objects.get(name = "semester") 
    semester.value = request.POST['semester']
    semester.save() 
    utils.log(f"semester changed to {semester.value}")
    messages.success(request,'semester changed succesfully')
    return redirect(reverse('admin_portal:dashboard'))
    

@is_admin
def activate(request):
    for student in models.Students.objects.all():
        student.activate()
    models.CurrentSemesterPayment.objects.all().delete() 
    messages.success(request, "activated succesfully")
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

@is_admin
def upload2(request):
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
            student.base_tuition_fee = request.POST["base_tuition_fee"]
            student.insurance_fee = request.POST["insurance_fee"]
            student.examination_fee = request.POST["examination_fee"]
            student.registration_fee = request.POST["registration_fee"]
            student.gymkhana_fee = request.POST["gymkhana_fee"]
            student.medical_fee = request.POST["medical_fee"]
            student.student_benevolent_fund = request.POST["student_benevolent_fund"]
            student.lab_fee = request.POST["lab_fee"]
            student.semester_mess_advance = request.POST["semester_mess_advance"]
            student.one_time_fee = request.POST["one_time_fee"]
            student.refundable_security_deposit = request.POST["refundable_security_deposit"]
            student.accommodation_charges = request.POST["accommodation_charges"]
            student.student_welfare_fund = request.POST["student_welfare_fund"]
            student.mess_rebate = request.POST["mess_rebate"]
            student.fee_arrear = request.POST["fee_arrear"]
            student.fee_paid = request.POST["fee_paid"]
            student.save()
            messages.success(request, "Student added successfully")
            utils.log(f"Student {student.roll_number} added")
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
        messages.error(request, e)
        return redirect(reverse("admin_portal:list"))


@is_admin
def delete(request):
    if request.method == "POST":
        try:
            excel_file = request.FILES["excel_file"]
            status = utils.excel_delete(excel_file)
            if(status['success'] > 0):
                messages.success(request,f"{status['success']} deletes succesfully")
            if(status['fail'] > 0):
                messages.error(request,f"{status['fail']} deletes failed / not found")
            utils.log("deleted students, reference: uploaded excel")
            return render(request, "admin_portal/delete.html")  
        except Exception as e:
            messages.error(request, "incorrect formatting")
            return redirect(reverse('admin_portal:delete'))
    else:
        return render(request, "admin_portal/delete.html")  



########## Fee Remission ##########
@is_admin
def remission(request):
    if request.method == "POST":
        try:
            roll_number = request.POST["roll_number"]
            remission_percentage = request.POST["remission_percentage"]
            utils.set_remission(roll_number, int(remission_percentage))
            utils.log("fee remission updated")
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
            utils.log("Cleared Fee Remissions")
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
        utils.log(f"fee remission for {id} deleted")
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
        utils.log("Added remission for students, reference: uploaded excel file")
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


########## Downloading student list ##########
def download_students_excel(request):
    df = utils.export_students()
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=students.xlsx"
    df.to_excel(response, index=False)
    return response


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
                utils.log(f"fee structure of {fee_structure_instance.course} : {fee_structure_instance.category} updated")
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
                utils.log(f"added fee structure for {fee_structure_instance.course} : {fee_structure_instance.category}")
                messages.success(
                    request, f"fee structure of {update_count} updated successfully"
                )
                return redirect(reverse("admin_portal:structure"))
            except Exception as e:
                print(e)
                messages.error(request, "incorrect formatting")
                return redirect(reverse("admin_portal:structure"))
    else:
        return render(
            request, "admin_portal/structure.html", {"fee_structures": fee_structures}
        )

@is_admin
def delete_structure(request,id): 
    try: 
        fee_structure_instance = models.FeeStructure.objects.get(id = id) 
        fee_structure_instance.delete()
        utils.log(f"fee structure of {fee_structure_instance.course} : {fee_structure_instance.category} deleted")
        messages.success(request,"deleted succesfully")
    except:
        messages.error(request,"could not find the specified entry")
    return redirect(reverse("admin_portal:structure"))

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
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        utils.log(f"updated details of {roll_number}")
        messages.success(request, "fee updated succesfully")
        return redirect(reverse("admin_portal:profile", args=[roll_number]))
    else:
        messages.error(request, "invalid input")
        return redirect(reverse("admin_portal:profile", args=[roll_number]))


########## Download Excel ##########
def download_excel(request, id):
    id += ".xlsx"
    excel_file_path = os.path.join(settings.BASE_DIR, "static", "excel", id)
    try:
        with open(excel_file_path, "rb") as excel_file:
            response = HttpResponse(
                excel_file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{id}"'
            return response
    except FileNotFoundError:
        print("File not found:", excel_file_path)
        return HttpResponse("File not found.", status=404)
    except Exception as e:
        print("An error occurred:", e)
        return HttpResponse("An error occurred.", status=500)


########## Admin logs ##########
class logs(ListView):
    model = models.Log
    template_name = "admin_portal/logs.html"
    context_object_name = "logs"
    paginate_by = 100

    @method_decorator(is_admin)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-timestamp')



@require_POST
@is_admin
def upload_excel(request):
    excel_file = request.FILES["excel_file"]
    utils.add_students(excel_file)
    utils.log("Added students from uploaded excel file")
    return redirect(reverse("admin_portal:upload"))

@require_POST
@is_admin
def upload_excel2(request):
    excel_file = request.FILES["excel_file"]
    utils.add_students2(excel_file)
    utils.log("Added students from uploaded excel file(without fee details)")
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
