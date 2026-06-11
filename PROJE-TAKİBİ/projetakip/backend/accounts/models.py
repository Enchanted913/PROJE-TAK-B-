from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Yönetici'
        TEACHER = 'teacher', 'Öğretmen'
        STUDENT = 'student', 'Öğrenci'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    student_number = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fcm_token = models.CharField(max_length=512, blank=True)

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    @property
    def is_teacher(self):
        return self.role in (self.Role.TEACHER, self.Role.ADMIN)

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def display_role(self):
        return self.get_role_display()
