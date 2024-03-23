from django.urls import path 
from . import views

app_name = "admin_portal" # refer namespacing in django 

urlpatterns = [
    path("",views.login, name = "login"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path("upload", views.upload, name = "upload"), 
    path("delete/<str:roll_number>/",views.delete, name = "delete"), 
    path("list", views.list.as_view(), name = "list"), 
    path("logs", views.logs, name = "logs"), 
    path("upload_excel", views.upload_excel, name = "upload_excel"),
    path("logout", views.logout, name = "logout"), 
    path("not_authorized", views.not_authorized, name = "not_authorized"), 
    path("profile/<str:roll_number>/",views.profile,name = "profile"),
    path("structure",views.fee_structure_list, name = "structure"), 
]
