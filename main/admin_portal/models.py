from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Students(models.Model): 
    # student details 
    name = models.CharField(max_length = 35) 
    roll_number = models.CharField(max_length = 15) 
    course = models.CharField(max_length = 10) 
    department = models.CharField(max_length = 10)
    email = models.EmailField() 
    category = models.CharField(max_length = 15) 

    # fee details 
    tuition_fee = models.IntegerField()
    insurance_fee = models.IntegerField() 
    examination_fee = models.IntegerField()
    registration_fee = models.IntegerField() 
    gymkhana_fee = models.IntegerField() 
    medical_fee = models.IntegerField() 
    student_benevolent_fund = models.IntegerField() 
    lab_fee = models.IntegerField() 
    semester_mess_advance = models.IntegerField() 
    one_time_fee = models.IntegerField()
    refundable_security_deposit = models.IntegerField()
    accomodation_charges = models.IntegerField() 
    student_welfare_fund = models.IntegerField() 
    mess_rebate = models.IntegerField() 

class GatewayPayments(models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    transaction_id = models.CharField(max_length = 50) 
    amount = models.IntegerField() 

class LoanPayments(models.Model): 
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length = 50) 
    amount = models.IntegerField() 

