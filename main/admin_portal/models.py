from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Students(models.Model):
    # student details
    roll_number = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=35)
    course = models.CharField(max_length=10)
    category = models.CharField(max_length=15)
    department = models.CharField(max_length=10)

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
    accommodation_charges = models.IntegerField()
    student_welfare_fund = models.IntegerField()
    mess_rebate = models.IntegerField(default = 0)
    fee_arrear = models.IntegerField(default = 0) 
    # fee to be payed
    fee_payable = models.IntegerField(default = 0)

    @property
    def total_fee(self):
        percentage = 0 
        if hasattr(self,"remission"): 
            percentage = self.remission.percentage
        percentage = 100 - percentage 
        return (
            int(self.tuition_fee * percentage / 100) 
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

    def activate(self):
        self.fee_arrear += self.fee_payable 
        self.fee_payable = self.total_fee - self.mess_rebate + self.fee_arrear 
        # self.mess_rebate = 0 
        # self.one_time_fee = 0 
        # self.refundable_security_deposit = 0 
        self.save() 

class Payments(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50)
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
    fee_received = models.IntegerField() 
    mode = models.CharField(max_length = 20)
    type = models.CharField(max_length = 20)
    
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
            + self.mess_rebate
        )

    @property
    def fee_receivable(self):
        return self.total_fee - self.mess_rebate 

class CustomUser(AbstractUser):
    isAdmin = models.BooleanField(default=False)


class FeeStructure(models.Model):
    course = models.CharField(max_length=10)
    category = models.CharField(max_length=15)
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

class FeeRemission(models.Model):  
    student = models.OneToOneField(Students, on_delete = models.CASCADE, primary_key = True, related_name = "remission") 
    percentage = models.IntegerField()  