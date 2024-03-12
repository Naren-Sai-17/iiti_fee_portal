from django.urls import path 
from . import views

app_name = "student_portal" # refer namespacing in django 

urlpatterns = [
    path("",views.index, name = "index"),
    path("dashboard",views.dashboard, name = "dashboard"),
    path("logout",views.LogoutView.as_view(), name = "logout"),
]
