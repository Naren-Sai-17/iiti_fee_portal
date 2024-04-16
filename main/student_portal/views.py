from django.shortcuts import render, redirect
from django.urls import reverse
from num2words import num2words
from django.contrib.auth import logout as dj_logout
from .decorators import is_student
from django.http import HttpResponse, Http404
from admin_portal import models 
from django.conf import settings
import re 
from hashlib import sha512
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def get_student(email): 
    try: 
        roll_number_match = re.search(r"\d+", email.split("@")[0])
        roll_number = roll_number_match.group()
        student_instance = models.Students.objects.get(roll_number = roll_number) 
        return student_instance
    except: 
        return None

def generate_hash(data, salt):
    hashString = data["merchant_key"] + "|" + data["transaction_id"] + "|" + data["amount"] + "|" + data["product_info"] + "|" + data['first_name'] + "|" + data['email'] + "|" +"|" +"|" +"|" +"|" +"|" + "|" +"|" +"|" +"|" + "|" + salt
    return sha512(hashString.encode('utf-8')).hexdigest()

@is_student
def payment(request):
    try:
        email = request.user.email 
        student_instance = get_student(email) 
        if student_instance is None:  
            return redirect(reverse('student_portal:not_found'))
        salt = settings.PAYU_CONFIG.get('merchant_salt')
        base_url = request.build_absolute_uri('/')[:-1]
        data =  {
            'merchant_key' : settings.PAYU_CONFIG.get('merchant_key'),
            'transaction_id' : uuid4().hex,
            'amount' : str(student_instance.fee_payable),
            'product_info': 'IIT Indore',
            'first_name': student_instance.name, 
            'email': request.user.email,
            'surl' : base_url + reverse('student_portal:payment_success'), 
            'furl' : base_url + reverse('student_portal:payment_failure'),
            'student' : student_instance
        }
        data['hash'] = generate_hash(data,salt)
        return render(request,'student_portal/payment.html',context = data)
    except: 
        raise Http404

@csrf_exempt
def payment_success(request): 
    messages.success(request,"payment success")

    return HttpResponse("payment success") 

@csrf_exempt
def payment_failure(request): 
    print(request.POST)
    messages.error(request,"payment failed")
    return redirect(reverse('student_portal:dashboard'))

@is_student
def not_found(request): 
    return render(request,"student_portal/not_found.html") 

@is_student
def dashboard(request):
    try: 
        email = request.user.email 
        student_instance = get_student(email) 
        if student_instance is None:  
            return redirect(reverse('student_portal:not_found'))
        transactions = models.Payments.objects.filter(student = student_instance)
        context = {
            'student' : student_instance , 
            'transactions' : transactions
        }
        return render(request, "student_portal/dashboard.html", context)
    except Exception as e: 
        return HttpResponse(e)

@is_student
def profile(request):
    try:
        student = request.user
        email = student.email
        email = request.user.email 
        student_instance = get_student(email) 
        if student_instance is None:  
            return redirect(reverse('admin_portal:not_found'))
        else: 
            return render(request,'student_portal/student_details.html',
                          {'student_details': student_instance })
    except: 
        raise Http404

@is_student
def receipt(request,id):
    payment = models.Payments.objects.get(id = id)
    context = {
        "receipt_no": payment.receipt_number,
        "roll_number": payment.student.roll_number,
        "name": payment.student.name,
        "date": payment.date,  
        "year":payment.date.year,
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
        "fee_receivable":payment.total_fee-payment.mess_rebate,
        "fee_payable":payment.fee_payable,
        "fee_received": payment.fee_received,
        "fee_paid":payment.student.fee_paid,
        "amtInWords": num2words(payment.student.fee_paid).upper(),
        "mode": payment.mode,
        "type": payment.type,

    }
    return render(request, "student_portal/receipt.html", context)


# views.py
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