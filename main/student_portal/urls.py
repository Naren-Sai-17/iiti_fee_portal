from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    path('payment_success',views.payment_success,name = 'payment_success'), 
    path('payment_failure', views.payment_failure, name ='payment_failure'), 
    path('not_found',views.not_found,name = 'not_found'), 
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

