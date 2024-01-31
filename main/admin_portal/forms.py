from django import forms 
from . import models 
class LoginForm(forms.Form): 
    session_username = forms.CharField(label = "Session username", max_length = 50) 
    admin_password = forms.CharField(label = "Admin password", widget=forms.PasswordInput)

class StudentSheetUploadForm(forms.Form):
    student_upload_sheet = forms.FileField() 