from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Students)
admin.site.register(Payments)
admin.site.register(CustomUser,UserAdmin) 
admin.site.register(FeeStructure)
admin.site.register(PaymentComponents)
admin.site.register(CurrentSemesterPayment)
admin.site.register(Variable)
