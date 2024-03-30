from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as dj_logout
from allauth.account.views import LogoutView 
from .decorators import is_student
from django.http import HttpResponse
from admin_portal.models import Students

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
