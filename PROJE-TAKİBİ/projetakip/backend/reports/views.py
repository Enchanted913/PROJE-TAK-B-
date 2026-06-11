from datetime import datetime
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from accounts.decorators import teacher_required
from accounts.models import User
from projects.models import Project, TaskProgress


@teacher_required
def report_list(request):
    projects = Project.objects.filter(teacher=request.user).prefetch_related('students')
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    student_id = request.GET.get('student', '')

    if status_filter:
        projects = projects.filter(status=status_filter)
    if date_from:
        projects = projects.filter(created_at__date__gte=date_from)
    if date_to:
        projects = projects.filter(created_at__date__lte=date_to)
    if student_id:
        projects = projects.filter(students__id=student_id)

    rows = []
    for project in projects.distinct():
        for student in project.students.all():
            completed = TaskProgress.objects.filter(
                task__project=project,
                student=student,
                status=TaskProgress.Status.COMPLETED,
            ).count()
            total = project.tasks.count()
            grade = project.grades.filter(student=student).first()
            rows.append({
                'project': project,
                'student': student,
                'completed': completed,
                'total': total,
                'score': grade.score if grade else '-',
            })

    students = User.objects.filter(role=User.Role.STUDENT, student_projects__teacher=request.user).distinct()
    chart_data = {
        'active': projects.filter(status=Project.Status.ACTIVE).count(),
        'partial': projects.filter(status=Project.Status.PARTIAL).count(),
        'completed': projects.filter(status=Project.Status.COMPLETED).count(),
    }

    return render(request, 'reports/report_list.html', {
        'rows': rows,
        'students': students,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'student_id': student_id,
        'chart_data': chart_data,
        'status_choices': Project.Status.choices,
    })


@teacher_required
def report_pdf(request):
    projects = Project.objects.filter(teacher=request.user)
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_filter:
        projects = projects.filter(status=status_filter)
    if date_from:
        projects = projects.filter(created_at__date__gte=date_from)
    if date_to:
        projects = projects.filter(created_at__date__lte=date_to)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [
        Paragraph('Proje Takip Raporu', styles['Title']),
        Paragraph(f'Oluşturulma: {timezone.now().strftime("%d.%m.%Y %H:%M")}', styles['Normal']),
        Spacer(1, 12),
    ]

    data = [['Proje', 'Öğrenci', 'Tamamlanan', 'Toplam', 'Puan', 'Durum']]
    for project in projects.distinct():
        for student in project.students.all():
            completed = TaskProgress.objects.filter(
                task__project=project, student=student, status=TaskProgress.Status.COMPLETED,
            ).count()
            total = project.tasks.count()
            grade = project.grades.filter(student=student).first()
            data.append([
                project.title,
                student.get_full_name() or student.username,
                str(completed),
                str(total),
                str(grade.score) if grade else '-',
                project.get_status_display(),
            ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
    ]))
    elements.append(table)
    doc.build(elements)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proje-raporu.pdf"'
    return response
