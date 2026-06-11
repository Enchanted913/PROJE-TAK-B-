from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import User


def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_teacher:
            messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)

    return wrapper


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_student:
            messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)

    return wrapper
