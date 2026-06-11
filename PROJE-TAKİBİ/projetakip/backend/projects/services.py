from django.conf import settings
from django.utils import timezone

from .models import Project, Task, TaskProgress


def ensure_task_progress(project: Project):
    """Her öğrenci-görev çifti için ilerleme kaydı oluştur."""
    for student in project.students.all():
        for task in project.tasks.all():
            TaskProgress.objects.get_or_create(task=task, student=student)


def update_project_status(project: Project):
    progresses = TaskProgress.objects.filter(task__project=project)
    total = progresses.count()
    if total == 0:
        return
    completed = progresses.filter(status=TaskProgress.Status.COMPLETED).count()
    if completed == total:
        project.status = Project.Status.COMPLETED
        project.completed_at = timezone.now()
    elif completed > 0:
        project.status = Project.Status.PARTIAL
    else:
        project.status = Project.Status.ACTIVE
    project.save(update_fields=['status', 'completed_at'])


def send_overdue_notifications():
    """Vadesi geçen görevler için FCM bildirimi gönder."""
    from accounts.models import User
    from .firebase import send_push_notification

    today = timezone.now().date()
    overdue_tasks = Task.objects.filter(due_date__lt=today, project__status=Project.Status.ACTIVE)
    for task in overdue_tasks:
        for student in task.project.students.all():
            progress = TaskProgress.objects.filter(task=task, student=student).first()
            if progress and progress.status != TaskProgress.Status.COMPLETED:
                if student.fcm_token:
                    send_push_notification(
                        student.fcm_token,
                        'Geciken Görev',
                        f'"{task.title}" görevinin son tarihi geçti!',
                    )


def check_completion_threshold(project: Project, threshold: int = 80):
    """Tamamlanma oranı eşiği aşıldığında öğretmene bildirim."""
    from .firebase import send_push_notification

    pct = project.completion_percentage()
    if pct >= threshold and project.teacher.fcm_token:
        send_push_notification(
            project.teacher.fcm_token,
            'Proje İlerlemesi',
            f'"{project.title}" projesi %{pct} tamamlandı.',
        )
