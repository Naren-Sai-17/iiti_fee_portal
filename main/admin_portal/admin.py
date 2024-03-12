from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Students)
admin.site.register(GatewayPayments)
admin.site.register(LoanPayments)
admin.site.register(CustomUser,UserAdmin) 
