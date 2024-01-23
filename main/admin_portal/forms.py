from django import forms 

class LoginForm(forms.Form): 
    session_username = forms.CharField(label = "Session username", max_length = 50) 
    admin_password = forms.CharField(label = "Admin password", widget=forms.PasswordInput)
