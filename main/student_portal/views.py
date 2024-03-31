from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as dj_logout
from allauth.account.views import LogoutView 
from .decorators import is_student
from django.http import HttpResponse
from admin_portal.models import Students
from admin_portal.models import GatewayPayments

# Create your views here.
def index(request): 
    if request.user.is_authenticated: 
        return redirect(reverse("student_portal:dashboard"))
    return render(request, "student_portal/login.html")

@is_student
def dashboard(request): 
    return render(request, 'student_portal/dashboard.html')

def logout(request): 
    dj_logout(request) 
    return redirect(reverse("student_portal:login"))

def not_authorized(request): 
    return render(request,"student_portal/not_authorized.html")

# def generate_receipt(request): 
    # return HttpResponse()
# print(type(current_student))


# def display_student_details(request):
#     current_student = request.user
   
#     email = current_student.email
#     roll_number = "220001049"
#     student_details = Students.objects.get(roll_number=roll_number)
#     return render(request, 'student_portal/student_details.html', {'student_details': student_details})




# import re

# def display_student_details(request):
#     try:
#         # Get the current user's email
#         current_student = request.user
#         email = current_student.email


#         # Use regular expressions to extract the numeric part after ignoring alphabets and everything after '@'
#         roll_number_match = re.search(r'\d+', email.split('@')[0])
#         if roll_number_match:
#             roll_number = roll_number_match.group()
#             # Query the Students model using the extracted roll number
#             try:
#                 student_details = Students.objects.get(roll_number=roll_number)
#                 return render(request, 'student_portal/student_details.html', {'student_details': student_details})
#             except Students.DoesNotExist:
#                 return HttpResponse("Student details not found.")
#         else:
#             return HttpResponse("Roll number not found in email.")
#     except Exception as e:
#         # Handle exceptions, such as if the email format is incorrect
#         print("An error occurred:", str(e))
#         return HttpResponse("An error occurred while processing the request.")


import hashlib
import re


def display_student_details(request):
    try:
        # Get the current user's email
        current_student = request.user
        email = current_student.email

        # Use regular expressions to extract the numeric part after ignoring alphabets and everything after '@'
        roll_number_match = re.search(r'\d+', email.split('@')[0])
        if roll_number_match:
            roll_number = roll_number_match.group()
            # Query the Students model using the extracted roll number
            try:
                student_details = Students.objects.get(roll_number=roll_number)
                
                # Fetching profile photo URL from Gravatar
                profile_photo_url = get_gravatar_url(email)
                
                return render(request, 'student_portal/student_details.html', {
                    'student_details': student_details,
                    'profile_photo_url': profile_photo_url  # Passing profile photo URL to the template
                })
            except Students.DoesNotExist:
                return HttpResponse("Student details not found.")
        else:
            return HttpResponse("Roll number not found in email.")
    except Exception as e:
        # Handle exceptions, such as if the email format is incorrect
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return HttpResponse(error_message)

# Function to get the Gravatar image URL based on the email address
def get_gravatar_url(email):
    hash_value = hashlib.md5(email.lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?d=identicon&s=200"





def generate_receipts(request):
    # Retrieve all student objects from the database
    current_student = request.user
    email = current_student.email
    # Use regular expressions to extract the numeric part after ignoring alphabets and everything after '@'
    roll_number_match = re.search(r'\d+', email.split('@')[0])
    roll_number = roll_number_match.group()
    student = Students.objects.get(roll_number=roll_number)
    student_data = GatewayPayments.objects.get(student=student)
    print(student_data)

    context ={
            'receipt_no': student_data.receipt_number,
            # Dummy receipt number
            'roll_number':roll_number,
            'name':student.name,
            'date': student_data.date,  # Dummy date
            'course':student.course,
            'category':student.category,
            'department':student.department,
            'tuition_fee': student_data.tuition_fee,
            'insurance_fee': student_data.insurance_fee,
            'examination_fee': student_data.examination_fee,
            'registration_fee': student_data.registration_fee,
            'gymkhana_fee': student_data.gymkhana_fee,
            'medical_fee': student_data.medical_fee,
            'student_benevolent_fund': student_data.student_benevolent_fund,
            'lab_fee': student_data.lab_fee,
            'semester_mess_advance': student_data.semester_mess_advance,
            'one_time_fee': student_data.one_time_fee,
            'refundable_security_deposit': student_data.refundable_security_deposit,
            'accommodation_charges': student_data.accommodation_charges,
            'student_welfare_fund': student_data.student_welfare_fund,
            'fee_arrear': student_data.fee_arrear,
            'mess_rebate': student_data.mess_rebate,
            'total_fee':student_data.total_fee,
            'fee_received': student_data.fee_received,
            
            'mode': student_data.mode,
            'type': student_data.type,
    }
    print(context)
    return render(request, 'student_portal/receipt.html', context)

# views.py

  # Assuming you have a Student model
from django.template.loader import render_to_string


def generate_re(request):
    # Get all students
    students = Students.objects.all()  # Update with your actual query to get all students
    
    # Prepare receipt data for each student
    receipts = []
    for student in students:
        # Here, you would generate receipt data for each student
        # You can use the student data along with any other relevant data to generate the receipts
        
        # Example: Generating receipt data for each student
        receipt_data = {
            'student_name': student.name,
            'tuition_fee': 1000,  # Example tuition fee amount
            # Add other receipt data as needed
        }
        
        # Render receipt HTML using the receipt_data
        receipt_html = render_to_string('receipt.html', receipt_data)
        
        # Append the rendered receipt HTML to the receipts list
        receipts.append(receipt_html)
    
    # Join all receipt HTMLs into a single string
    all_receipts_html = '\n'.join(receipts)
    
    # Return HTTP response with all receipts HTML
    return HttpResponse(all_receipts_html)
