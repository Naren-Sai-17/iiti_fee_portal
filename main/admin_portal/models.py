from django.db import models
from django.contrib.auth.models import AbstractUser

class Students(models.Model): 
    # student details 
    roll_number = models.CharField(max_length = 15, primary_key = True) 
    name = models.CharField(max_length = 35) 
    course = models.CharField(max_length = 10) 
    category = models.CharField(max_length = 15) 
    department = models.CharField(max_length = 10)
    # email = models.EmailField() 

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

    @property
    def total_fee(self):
        return(
            self.tuition_fee +
            self.insurance_fee + 
            self.examination_fee + 
            self.registration_fee + 
            self.gymkhana_fee + 
            self.medical_fee + 
            self.student_benevolent_fund + 
            self.lab_fee + 
            self.semester_mess_advance + 
            self.one_time_fee +
            self.refundable_security_deposit +
            self.accomodation_charges + 
            self.student_welfare_fund + 
            self.mess_rebate 
        )
    
    @property 
    def fee_receivable(self): 
        return self.total_fee - self.mess_rebate

class GatewayPayments(models.Model):
    student = models.ForeignKey(Students, on_delete = models.CASCADE)
    transaction_id = models.CharField(max_length = 50) 
    amount = models.IntegerField() 

class LoanPayments(models.Model): 
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length = 50) 
    amount = models.IntegerField() 
 
class CustomUser(AbstractUser): 
    isAdmin = models.BooleanField(default = False) 