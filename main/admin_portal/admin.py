from django.contrib import admin
from .models import *

admin.site.register(Students)
admin.site.register(GatewayPayments)
admin.site.register(LoanPayments)
admin.site.register(CustomUser) 
