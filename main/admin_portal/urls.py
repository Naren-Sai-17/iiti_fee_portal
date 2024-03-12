from django.urls import path 
from . import views

app_name = "admin_portal" # refer namespacing in django 

urlpatterns = [
    path("",views.login, name = "login"),
    path("base", views.base, name = "base"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path("upload", views.upload, name = "upload"), 
    path("list", views.list.as_view(), name = "list"), 
    path("logs", views.logs, name = "logs"), 
    path("upload_excel", views.upload_excel, name = "upload_excel"),
    path("logout", views.logout, name = "logout"), 
    path("not_authorized", views.not_authorized, name = "not_authorized"), 
]
