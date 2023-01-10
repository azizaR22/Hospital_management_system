from django.http import HttpResponse
from django.shortcuts import redirect


def unautherized_user(view_func):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_fun


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwarge):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwarge)
            else:
                return HttpResponse("you are not allowed to see this page")

        return wrapper_func

    return decorator
