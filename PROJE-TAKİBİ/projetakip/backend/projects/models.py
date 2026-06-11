from django.conf import settings
from django.db import models
from django.utils import timezone


class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Devam Ediyor'
        COMPLETED = 'completed', 'Tamamlandı'
        PARTIAL = 'partial', 'Yarım Kaldı'

    title = models.CharField(max_length=200, verbose_name='Proje adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teaching_projects',
        verbose_name='Öğretmen',
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student_projects',
        blank=True,
        limit_choices_to={'role': 'student'},
        verbose_name='Öğrenciler',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Proje'
        verbose_name_plural = 'Projeler'

    def __str__(self):
        return self.title

    @property
    def completed_task_count(self):
        return TaskProgress.objects.filter(task__project=self, status=TaskProgress.Status.COMPLETED).count()

    @property
    def total_task_count(self):
        return self.tasks.count()

    def completion_percentage(self):
        total = self.total_task_count * max(self.students.count(), 1)
        if total == 0:
            return 0
        return round((self.completed_task_count / total) * 100, 1)


class ProjectGrade(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_grades',
        limit_choices_to={'role': 'student'},
    )
    score = models.PositiveSmallIntegerField(verbose_name='Puan')
    note = models.TextField(blank=True, verbose_name='Not')

    class Meta:
        unique_together = ('project', 'student')
        verbose_name = 'Proje Puanı'
        verbose_name_plural = 'Proje Puanları'

    def __str__(self):
        return f'{self.project} - {self.student} ({self.score})'


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name='Görev adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    due_date = models.DateField(null=True, blank=True, verbose_name='Son tarih')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Görev'
        verbose_name_plural = 'Görevler'

    def __str__(self):
        return self.title

    def is_overdue(self):
        if not self.due_date:
            return False
        return self.due_date < timezone.now().date()


class TaskProgress(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Başlanmadı'      # kırmızı
        IN_PROGRESS = 'in_progress', 'Devam Ediyor'    # sarı
        COMPLETED = 'completed', 'Tamamlandı'          # yeşil

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress_records')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_progress',
        limit_choices_to={'role': 'student'},
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('task', 'student')
        verbose_name = 'Görev İlerlemesi'
        verbose_name_plural = 'Görev İlerlemeleri'

    def __str__(self):
        return f'{self.task} - {self.student} ({self.get_status_display()})'

    @property
    def status_color(self):
        return {
            self.Status.NOT_STARTED: 'danger',
            self.Status.IN_PROGRESS: 'warning',
            self.Status.COMPLETED: 'success',
        }.get(self.status, 'secondary')
