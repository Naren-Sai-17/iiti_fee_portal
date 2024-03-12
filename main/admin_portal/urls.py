from django.urls import path 
from . import views

app_name = "admin_portal" # refer namespacing in django 

urlpatterns = [
    path("",views.login, name = "login"),
    path("base", views.base, name = "base"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path("upload", views.upload, name = "upload"), 
    path("loan", views.loan, name = "loan"),
    path("list", views.list.as_view(), name = "list"), 
    path("logs", views.logs, name = "logs"), 
    path("upload_excel", views.upload_excel, name = "upload_excel"),
    path("loan_excel", views.loan_excel, name = "loan_excel")
]
