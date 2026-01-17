from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role not in allowed_roles and not request.user.is_admin:
                return HttpResponseForbidden("Доступ запрещен")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_admin:
            return HttpResponseForbidden("Требуются права администратора")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_regular_user and not request.user.is_admin:
            return HttpResponseForbidden("Требуется регистрация")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view