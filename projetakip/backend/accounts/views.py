from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomPasswordResetForm, LoginForm, RegisterForm, StudentForm
from .decorators import teacher_required
from .models import User


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = CustomPasswordResetForm


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Kayıt başarılı. Giriş yapabilirsiniz.')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.is_teacher:
        return redirect('projects:teacher_dashboard')
    return redirect('projects:student_dashboard')


@teacher_required
def student_list(request):
    students = User.objects.filter(role=User.Role.STUDENT).order_by('last_name', 'first_name')
    return render(request, 'accounts/student_list.html', {'students': students})


@teacher_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not form.cleaned_data.get('password'):
                user.set_password('ogrenci123')
            else:
                user.set_password(form.cleaned_data['password'])
            user.role = User.Role.STUDENT
            user.save()
            messages.success(request, 'Öğrenci eklendi.')
            return redirect('accounts:student_list')
    else:
        form = StudentForm()
    return render(request, 'accounts/student_form.html', {'form': form, 'title': 'Öğrenci Ekle'})


@teacher_required
def student_edit(request, pk):
    student = User.objects.get(pk=pk, role=User.Role.STUDENT)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Öğrenci güncellendi.')
            return redirect('accounts:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'accounts/student_form.html', {'form': form, 'title': 'Öğrenci Düzenle'})


@teacher_required
def student_delete(request, pk):
    student = User.objects.get(pk=pk, role=User.Role.STUDENT)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Öğrenci silindi.')
        return redirect('accounts:student_list')
    return render(request, 'accounts/student_confirm_delete.html', {'student': student})
