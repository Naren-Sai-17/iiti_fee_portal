from django.urls import path 
from . import views

app_name = "admin_portal" # refer namespacing in django 

urlpatterns = [
    path("",views.index, name = "index"),
    path("base", views.base, name = "base"),
    path("dashboard", views.dashboard, name = "dashboard")
]
