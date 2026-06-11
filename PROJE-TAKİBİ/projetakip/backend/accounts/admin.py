from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'student_number', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Ek Bilgiler', {'fields': ('role', 'student_number', 'phone', 'fcm_token')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Ek Bilgiler', {'fields': ('role', 'student_number', 'phone')}),
    )
