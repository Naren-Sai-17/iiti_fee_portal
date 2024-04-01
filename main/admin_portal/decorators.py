from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def is_admin(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.isAdmin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse("admin_portal:not_authorized"))
    return wrapped_view
