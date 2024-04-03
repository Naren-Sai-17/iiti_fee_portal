from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as dj_logout
from .decorators import is_student
from django.http import HttpResponse, Http404
from admin_portal import models 
import re 

@is_student
def dashboard(request):
    try: 
        student = request.user
        email = student.email
        roll_number_match = re.search(r"\d+", email.split("@")[0])
        roll_number = roll_number_match.group()
        student_instance = models.Students.objects.get(roll_number = roll_number)
        transactions = models.Payments.objects.filter(student = student_instance)
        return render(request, "student_portal/dashboard.html", {'transactions' : transactions })
    except Exception as e: 
        return HttpResponse(e)

@is_student
def profile(request):
    try:
        student = request.user
        email = student.email
        roll_number_match = re.search(r"\d+", email.split("@")[0])
        if roll_number_match:
            roll_number = roll_number_match.group()
            try:
                student_details = models.Students.objects.get(roll_number=roll_number)
                return render(
                    request,
                    "student_portal/student_details.html",
                    {
                        "student_details": student_details,
                    },
                )
            except models.Students.DoesNotExist:
                return HttpResponse("Student details not found.")
        else:
            return HttpResponse("Roll number not found in email.")
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return HttpResponse(error_message)

@is_student
def receipt(request,id):
    payment = models.Payments.objects.get(id = id)
    context = {
        "receipt_no": payment.receipt_number,
        # Dummy receipt number
        "roll_number": payment,
        "name": payment.student.name,
        "date": payment.date,  # Dummy date
        "course": payment.student.course,
        "category": payment.student.category,
        "department": payment.student.department,
        "tuition_fee": payment.tuition_fee,
        "insurance_fee": payment.insurance_fee,
        "examination_fee": payment.examination_fee,
        "registration_fee": payment.registration_fee,
        "gymkhana_fee": payment.gymkhana_fee,
        "medical_fee": payment.medical_fee,
        "student_benevolent_fund": payment.student_benevolent_fund,
        "lab_fee": payment.lab_fee,
        "semester_mess_advance": payment.semester_mess_advance,
        "one_time_fee": payment.one_time_fee,
        "refundable_security_deposit": payment.refundable_security_deposit,
        "accommodation_charges": payment.accommodation_charges,
        "student_welfare_fund": payment.student_welfare_fund,
        "fee_arrear": payment.fee_arrear,
        "mess_rebate": payment.mess_rebate,
        "total_fee": payment.total_fee,
        "fee_received": payment.fee_received,
        "mode": payment.mode,
        "type": payment.type,
    }
    return render(request, "student_portal/receipt.html", context)


# views.py

# Assuming you have a Student model
from django.template.loader import render_to_string


# def generate_re(request):
#     # Get all students
#     students = (
#         Students.objects.all()
#     )  # Update with your actual query to get all students

#     # Prepare receipt data for each student
#     receipts = []
#     for student in students:
#         # Here, you would generate receipt data for each student
#         # You can use the student data along with any other relevant data to generate the receipts

#         # Example: Generating receipt data for each student
#         receipt_data = {
#             "student_name": student.name,
#             "tuition_fee": 1000,  # Example tuition fee amount
#             # Add other receipt data as needed
#         }

#         # Render receipt HTML using the receipt_data
#         receipt_html = render_to_string("receipt.html", receipt_data)

#         # Append the rendered receipt HTML to the receipts list
#         receipts.append(receipt_html)

#     # Join all receipt HTMLs into a single string
#     all_receipts_html = "\n".join(receipts)

#     # Return HTTP response with all receipts HTML
#     return HttpResponse(all_receipts_html)

## authentication 
    
def index(request):
    if request.user.is_authenticated:
        return redirect(reverse("student_portal:dashboard"))
    return render(request, "student_portal/login.html")

def logout(request):
    dj_logout(request)
    return redirect(reverse("student_portal:login"))

def not_authorized(request):
    return render(request, "student_portal/not_authorized.html")