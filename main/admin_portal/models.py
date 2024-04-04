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
    mess_rebate = models.IntegerField(default = 0)
    fee_arrear = models.IntegerField(default = 0) 
    # fee to be payed
    fee_payable = models.IntegerField(default = 0)

    @property 
    def tuition_fee(self): 
        # add remission logic 
        return self.base_tuition_fee 
    
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

    def activate(self):
        self.fee_arrear += self.fee_payable 
        self.fee_payable = self.total_fee - self.mess_rebate
        # self.mess_rebate = 0 
        # self.one_time_fee = 0 
        # self.refundable_security_deposit = 0 
        self.save() 

    def make_payment(self,amt): 
        # create a new payment 
        payment = Payments() 
        payment.student = self 
        # payment.receipt_number
        # payment.date 
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
        
        payment.mode = "DUMMY"
        payment.type = "DUMMY" 
        payment.save() 

        # update the student details 
        self.fee_arrear = payment.fee_payable + payment.fee_arrear - payment.fee_received
        self.fee_payable = 0
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
    fee_payable = models.IntegerField()
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
    percentage = models.IntegerField()  

class Log(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class studentStats(models.Model):  
    student = models.OneToOneField(Students, on_delete = models.CASCADE, primary_key = True, related_name = "stats") 
    hasReceipt = models.BooleanField(default=False)  





