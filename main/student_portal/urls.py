from django.urls import path 
from . import views

app_name = "student_portal" # refer namespacing in django 


# student_portal/urls.py


urlpatterns = [
    path("",views.index, name = "login"),
    path("dashboard",views.dashboard, name = "dashboard"),
    path("logout",views.logout, name = "logout"),
    path("not_authorized",views.not_authorized, name = "not_authorized"),
    path('profile/', views.profile, name='profile'),
    path('receipt/<int:id>/', views.receipt, name='receipt'), 
    path('payment',views.payment, name = 'payment'), 
]
