from django import forms 
from . import models 
class LoginForm(forms.Form): 
    username = forms.CharField(label="username" ,  max_length=50, widget=forms.TextInput(attrs={ 'class': 'block text-sm font-medium leading-6 text-[#0369a1]' 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder: px-3 text-gray-400 focus:ring-2 focus:ring-inset focus:ring-[#0284c7] sm:text-sm sm:leading-6 ' , 'placeholder':'username'})) 
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'block w-full font-medium rounded-md border-0 py-1.5 text-[#0369a1] shadow-sm ring-1 ring-inset ring-gray-300 placeholder: px-3 text-gray-400  focus:ring-inset focus:ring-2 focus:ring-[#0284c7] sm:text-sm sm:leading-6 ' , 'placeholder':'password'}))
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
        fields = '__all__'

