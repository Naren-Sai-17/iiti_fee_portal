from django.urls import path 
from . import views

app_name = "admin_portal" # refer namespacing in django 

urlpatterns = [
    path("make_payment", views.make_payment, name = "make_payment"), 
    path("dashboard", views.dashboard, name = "dashboard"),
    path("set_semester",views.set_semester, name = "set_semester"), 
    path("activate", views.activate, name = "activate"), 
    path("loan",views.loan, name = "loan"), 
    # remission  
    path("remission",views.remission,name = "remission"),
    path("group_remission", views.group_remission, name = "group_remission"),
    path("delete_remission/<str:id>/", views.delete_remission, name = "delete_remission"), 
    path("clear_remission", views.clear_remission,name = "clear_remission"),
    path("logs", views.logs.as_view(), name = "logs"), 
    path("download_excel/<str:id>/",views.download_excel, name = "download_excel"), 
    path("structure",views.fee_structure_list, name = "structure"), 
    path("delete_structure/<str:id>/",views.delete_structure, name = "delete_structure"), 
    # student management 
    path("delete_student/<str:roll_number>/",views.delete_student, name = "delete_student"),
    path("delete", views.delete, name = "delete"), 
    path("upload", views.upload, name = "upload"), 
    path("upload_excel", views.upload_excel, name = "upload_excel"),
    path("upload_excel2", views.upload_excel2, name = "upload_excel2"),
    path("profile/<str:roll_number>/",views.profile,name = "profile"),
    path("update_profile", views.update_profile, name='update_profile'),
    path("list", views.list.as_view(), name = "list"), 
    path('download/students/excel/', views.download_students_excel, name='download_students_excel'),

    # authorization 
    path("",views.login, name = "login"),
    path("logout", views.logout, name = "logout"), 
    path("not_authorized", views.not_authorized, name = "not_authorized"), 


]
