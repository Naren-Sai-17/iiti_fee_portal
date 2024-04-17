from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
import math

class Students(models.Model):
    # student details
    roll_number = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=35)
    course = models.CharField(max_length=10)
    category = models.CharField(max_length=15)
    department = models.CharField(max_length=10)

    # fee details
    base_tuition_fee = models.IntegerField()
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
    accommodation_charges = models.IntegerField()
    student_welfare_fund = models.IntegerField()

    # extra fee 
    mess_rebate = models.IntegerField(default = 0)
    fee_arrear = models.IntegerField(default = 0) 

    # fee payed in this semester 
    fee_paid = models.IntegerField(default = 0) 
    
    # derived attributes
    tuition_fee = models.IntegerField(default=0) 
    total_fee = models.IntegerField(default=0) 
    fee_payable = models.IntegerField(default=0)


    def save(self,*args,**kwargs): 
        tuition_fee_value = 0 
        if(hasattr(self,'remission')): 
            if self.remission.percentage == 1: 
                tuition_fee_value = 0
            else:
                tuition_fee_value =  self.base_tuition_fee - math.ceil(self.base_tuition_fee*2/3)
        else: 
            tuition_fee_value = self.base_tuition_fee

        total_fee_value = (
            tuition_fee_value
            + self.insurance_fee
            + self.examination_fee
            + self.registration_fee
            + self.gymkhana_fee
            + self.medical_fee
            + self.student_benevolent_fund
            + self.lab_fee
            + self.semester_mess_advance
            + self.one_time_fee
            + self.refundable_security_deposit
            + self.accommodation_charges
            + self.student_welfare_fund
        )

        fee_payable_value = total_fee_value - self.mess_rebate + self.fee_arrear - self.fee_paid

        self.tuition_fee = tuition_fee_value
        self.total_fee = total_fee_value
        self.fee_payable = fee_payable_value

        super().save(*args, **kwargs)

    def activate(self):
        self.fee_arrear = self.fee_payable 
        self.fee_paid = 0 
        self.mess_rebate = 0 
        self.one_time_fee = 0  
        self.refundable_security_deposit = 0
        self.save() 

    def make_payment(self,amt,mode,type,utr): 
        if not CurrentSemesterPayment.objects.filter(student = self).exists():    
            amt = int(amt)
            payment = Payments() 
            payment.student = self 
            payment.receipt_number = "temp"
            payment.date = datetime.now() 
            payment.tuition_fee = self.tuition_fee
            payment.insurance_fee = self.insurance_fee
            payment.examination_fee = self.insurance_fee
            payment.examination_fee = self.examination_fee
            payment.registration_fee = self.registration_fee
            payment.gymkhana_fee = self.gymkhana_fee
            payment.medical_fee = self.medical_fee
            payment.student_benevolent_fund = self.student_benevolent_fund
            payment.lab_fee = self.lab_fee
            payment.semester_mess_advance = self.semester_mess_advance
            payment.one_time_fee = self.one_time_fee
            payment.refundable_security_deposit = self.refundable_security_deposit
            payment.accommodation_charges = self.accommodation_charges
            payment.student_welfare_fund = self.student_welfare_fund
            payment.fee_arrear = self.fee_arrear 
            payment.mess_rebate = self.mess_rebate 
            payment.fee_payable = self.fee_payable
            payment.fee_received = amt 
            payment.save() 
            component = PaymentComponents(payment = payment, mode = mode,type = type, utr = utr)
            component.save() 

            # update the student details 
            self.fee_paid += amt
            self.save() 

            # add the current semester payment 
            current_semester_payment = CurrentSemesterPayment(student = self, payment = payment)
            current_semester_payment.save() 
        else: 
            # already a payment has been made just update it 
            payment.fee_received += amt
            self.fee_paid += amt 
            payment.save()
            self.save()  
            component = PaymentComponents(payment = payment, mode = mode,type = type, utr = utr)
            component.save() 


class Payments(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    semester = models.CharField(max_length = 30)
    date = models.DateField()
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
    accommodation_charges = models.IntegerField()
    student_welfare_fund = models.IntegerField()
    fee_arrear = models.IntegerField() 
    mess_rebate = models.IntegerField()
    fee_payable = models.IntegerField()
    fee_received = models.IntegerField() 
    
    @property
    def total_fee(self):
        return (
            self.tuition_fee
            + self.insurance_fee
            + self.examination_fee
            + self.registration_fee
            + self.gymkhana_fee
            + self.medical_fee
            + self.student_benevolent_fund
            + self.lab_fee
            + self.semester_mess_advance
            + self.one_time_fee
            + self.refundable_security_deposit
            + self.accommodation_charges
            + self.student_welfare_fund
        )

class PaymentComponents(models.Model):
    payment = models.ForeignKey(to = Payments,on_delete=models.CASCADE,related_name="components",primary_key=True)
    mode = models.CharField(max_length = 20)
    type = models.CharField(max_length = 50)
    utr = models.CharField(max_length=50)
    amt = models.IntegerField(default=0)
    


class CustomUser(AbstractUser):
    isAdmin = models.BooleanField(default=False)


class FeeStructure(models.Model):
    course = models.CharField(max_length=10)
    category = models.CharField(max_length=15)
    base_tuition_fee = models.IntegerField()
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
    accommodation_charges = models.IntegerField()
    student_welfare_fund = models.IntegerField()

class FeeRemission(models.Model):  
    student = models.OneToOneField(Students, on_delete = models.CASCADE, primary_key = True, related_name = "remission") 
    percentage = models.CharField(max_length=3,choices=(("1","1"),("2/3","2/3")))  

class Log(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Variable(models.Model): 
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30) 

class CurrentSemesterPayment(models.Model): 
    student = models.ForeignKey(Students,on_delete=models.CASCADE,primary_key=True)
    payment = models.OneToOneField(Payments,on_delete=models.CASCADE,related_name="csempayment") 

    