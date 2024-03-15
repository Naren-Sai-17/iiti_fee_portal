from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as dj_logout
from allauth.account.views import LogoutView 
from .decorators import is_student
from django.http import HttpResponse
# 
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
    return render(request,"not_authorized.html")

# print(type(current_student))


# def display_student_details(request):
#     current_student = request.user
   
#     email = current_student.email
#     roll_number = "220001049"
#     student_details = Students.objects.get(roll_number=roll_number)
#     return render(request, 'student_portal/student_details.html', {'student_details': student_details})

# import re
# from django.contrib.auth.models import User

# def display_student_details(request):
#     # Get the current user
#     current_user = request.user
#     email = current_user.email

#     # Use regular expressions to extract the roll number from the email address
#     roll_number_match = re.search(r'\d+', email)
#     if roll_number_match:
#         roll_number = roll_number_match.group()
#     else:
#         # Handle the case where roll number is not found
#         return HttpResponse("Roll number not found in email.")

#     # Query the Students model using the extracted roll number
#     try:
#         student_details = Students.objects.get(roll_number=roll_number)
#     except Students.DoesNotExist:
#         # Handle the case where the student with the given roll number does not exist
#         return HttpResponse("Student details not found.")

#     # Render the student details page with the retrieved student details
#     return render(request, 'student_portal/student_details.html', {'student_details': student_details})

# import re

# def display_student_details(email):
#     try:
#         # Use regular expressions to extract the numeric part after ignoring alphabets and everything after '@'
#         roll_number_match = re.search(r'\d+', email.split('@')[0])
#         if roll_number_match:
#             roll_number = roll_number_match.group()
#             # Query the Students model using the extracted roll number
#             try:
#                 student_details = Students.objects.get(roll_number=roll_number)
#                 return student_details
#             except Students.DoesNotExist:
#                 return None
#         else:
#             return None
#     except Exception as e:
#         # Handle exceptions, such as if the email format is incorrect
#         print("An error occurred while extracting student details:", str(e))
#         return None

# # Test the function with an example email
# email = "cse220001049@iiti.ac.in"
# student_details = display_student_details(email)
# if student_details:
#     print("Student Details:")
#     print("Roll Number:", student_details.roll_number)
#     print("Name:", student_details.name)
#     print("Course:", student_details.course)
#     print("Category:", student_details.category)
#     print("Department:", student_details.department)
# else:
#     print("Student details not found.")



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
                return render(request, 'student_portal/student_details.html', {'student_details': student_details})
            except Students.DoesNotExist:
                return HttpResponse("Student details not found.")
        else:
            return HttpResponse("Roll number not found in email.")
    except Exception as e:
        # Handle exceptions, such as if the email format is incorrect
        print("An error occurred:", str(e))
        return HttpResponse("An error occurred while processing the request.")

