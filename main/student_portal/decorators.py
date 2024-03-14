from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

def is_student(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (not request.user.isAdmin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse("student_portal:not_authorized"))
    return wrapped_view
