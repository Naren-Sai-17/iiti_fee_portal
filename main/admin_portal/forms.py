from django import forms 
from . import models 
class LoginForm(forms.Form): 
    username = forms.CharField(label="username" ,  max_length=50, widget=forms.TextInput(attrs={ 'class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#0369a1] focus:border-transparent',' placeholder':'Enter your username'})) 
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#0369a1] focus:border-transparent', 'placeholder':'Enter Password'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
   
class StudentUploadForm(forms.Form):
    student_upload_sheet = forms.FileField() 

class StudentAddForm(forms.Form): 
    roll_number = forms.CharField(max_length=15)
    name = forms.CharField(max_length=35)
    course = forms.CharField(max_length=10)
    category = forms.CharField(max_length=15)
    department = forms.CharField(max_length=10)

class FeeStructureForm(forms.ModelForm): 
    class Meta: 
        model = models.FeeStructure
        fields = '__all__'
        
class Profile(forms.ModelForm):
    class Meta:
        model=models.Students
        exclude = ['tuition_fee','total_fee','fee_payable']
