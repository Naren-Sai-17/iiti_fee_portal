from django.db import models
from django.contrib.auth.models import AbstractUser

class Students(models.Model): 
    roll_number = models.CharField(max_length = 15) 
    course = models.CharField

