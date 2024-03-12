from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

def is_admin(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.isAdmin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse("admin_portal:not_authorized"))
    return wrapped_view
