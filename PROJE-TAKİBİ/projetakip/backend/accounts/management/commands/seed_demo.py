from django.core.management.base import BaseCommand

from accounts.models import User
from projects.models import Project, Task
from projects.services import ensure_task_progress


class Command(BaseCommand):
    help = 'Demo öğretmen, öğrenci ve proje verisi oluşturur'

    def handle(self, *args, **options):
        teacher, _ = User.objects.get_or_create(
            username='ogretmen',
            defaults={
                'email': 'ogretmen@okul.edu.tr',
                'first_name': 'Ahmet',
                'last_name': 'Öğretmen',
                'role': User.Role.TEACHER,
            },
        )
        if not teacher.has_usable_password():
            teacher.set_password('ogretmen123')
            teacher.save()

        student, _ = User.objects.get_or_create(
            username='ogrenci1',
            defaults={
                'email': 'ogrenci1@okul.edu.tr',
                'first_name': 'Ayşe',
                'last_name': 'Yılmaz',
                'student_number': '2024001',
                'role': User.Role.STUDENT,
            },
        )
        if not student.has_usable_password():
            student.set_password('ogrenci123')
            student.save()

        project, created = Project.objects.get_or_create(
            title='Mobil Uygulama Projesi',
            teacher=teacher,
            defaults={'description': 'Flutter ile öğrenci takip uygulaması geliştirme.'},
        )
        project.students.add(student)
        if created or not project.tasks.exists():
            Task.objects.get_or_create(
                project=project, title='Arayüz tasarımı',
                defaults={'description': 'Ana ekranları tasarla', 'order': 1},
            )
            Task.objects.get_or_create(
                project=project, title='API entegrasyonu',
                defaults={'description': 'Django API bağlantısı', 'order': 2},
            )
        ensure_task_progress(project)
        self.stdout.write(self.style.SUCCESS('Demo veri hazır: ogretmen/ogretmen123, ogrenci1/ogrenci123'))
