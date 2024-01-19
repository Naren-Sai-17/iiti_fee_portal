from django.db import models
from django.contrib.auth.models import AbstractUser

class Students(models.Model): 
    name = models.CharField(max_length = 35) 
    roll_number = models.CharField(max_length = 15) 
    course = models.CharField(max_length = 10) 
    department = models.CharField(max_length = 10)
    email = models.EmailField() 
    category = models.CharField(max_length = 15) 


