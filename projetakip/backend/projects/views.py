import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import student_required, teacher_required
from accounts.models import User

from .forms import GradeForm, ProjectForm, TaskForm
from .models import Project, ProjectGrade, Task, TaskProgress
from .services import check_completion_threshold, ensure_task_progress, update_project_status


@teacher_required
def teacher_dashboard(request):
    projects = Project.objects.filter(teacher=request.user)
    stats = {
        'total': projects.count(),
        'active': projects.filter(status=Project.Status.ACTIVE).count(),
        'partial': projects.filter(status=Project.Status.PARTIAL).count(),
        'completed': projects.filter(status=Project.Status.COMPLETED).count(),
        'students': User.objects.filter(role=User.Role.STUDENT).count(),
    }
    chart_labels = ['Devam Eden', 'Yarım', 'Tamamlanan']
    chart_data = [stats['active'], stats['partial'], stats['completed']]
    return render(request, 'projects/teacher_dashboard.html', {
        'projects': projects[:5],
        'stats': stats,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    })


@student_required
def student_dashboard(request):
    projects = request.user.student_projects.all()
    return render(request, 'projects/student_dashboard.html', {'projects': projects})


@teacher_required
def project_list(request):
    projects = Project.objects.filter(teacher=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})


@teacher_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.teacher = request.user
            project.save()
            form.save_m2m()
            ensure_task_progress(project)
            messages.success(request, 'Proje oluşturuldu.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Proje Ekle'})


@teacher_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            ensure_task_progress(project)
            update_project_status(project)
            messages.success(request, 'Proje güncellendi.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Proje Düzenle'})


@teacher_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, teacher=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Proje silindi.')
        return redirect('projects:project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.is_student and request.user not in project.students.all():
        messages.error(request, 'Bu projeye erişiminiz yok.')
        return redirect('projects:student_dashboard')
    if request.user.is_teacher and project.teacher != request.user:
        messages.error(request, 'Bu projeye erişiminiz yok.')
        return redirect('projects:teacher_dashboard')

    tasks = project.tasks.all()
    progresses = TaskProgress.objects.filter(task__project=project)
    if request.user.is_student:
        progresses = progresses.filter(student=request.user)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'progresses': progresses,
    })


@teacher_required
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk, teacher=request.user)
    if request.method == 'POST':
        project.status = Project.Status.COMPLETED
        project.completed_at = timezone.now()
        project.save()
        messages.success(request, 'Proje tamamlandı olarak işaretlendi.')
        return redirect('projects:project_detail', pk=pk)
    return render(request, 'projects/project_complete.html', {'project': project})


@teacher_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, teacher=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            ensure_task_progress(project)
            messages.success(request, 'Görev eklendi.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'projects/task_form.html', {'form': form, 'project': project, 'title': 'Görev Ekle'})


@teacher_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, project__teacher=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Görev güncellendi.')
            return redirect('projects:project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'projects/task_form.html', {'form': form, 'project': task.project, 'title': 'Görev Düzenle'})


@teacher_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, project__teacher=request.user)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Görev silindi.')
        return redirect('projects:project_detail', pk=project_pk)
    return render(request, 'projects/task_confirm_delete.html', {'task': task})


@teacher_required
def grade_student(request, project_pk, student_pk):
    project = get_object_or_404(Project, pk=project_pk, teacher=request.user)
    student = get_object_or_404(User, pk=student_pk, role=User.Role.STUDENT)
    grade, _ = ProjectGrade.objects.get_or_create(project=project, student=student)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Puan kaydedildi.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = GradeForm(instance=grade)
    return render(request, 'projects/grade_form.html', {'form': form, 'project': project, 'student': student})


@student_required
def task_start(request, pk):
    progress = get_object_or_404(TaskProgress, pk=pk, student=request.user)
    if progress.status == TaskProgress.Status.NOT_STARTED:
        progress.status = TaskProgress.Status.IN_PROGRESS
        progress.started_at = timezone.now()
        progress.save()
        update_project_status(progress.task.project)
        messages.success(request, 'Göreve başladınız.')
    return redirect('projects:project_detail', pk=progress.task.project.pk)


@student_required
def task_complete(request, pk):
    progress = get_object_or_404(TaskProgress, pk=pk, student=request.user)
    progress.status = TaskProgress.Status.COMPLETED
    progress.completed_at = timezone.now()
    if not progress.started_at:
        progress.started_at = timezone.now()
    progress.save()
    project = progress.task.project
    update_project_status(project)
    check_completion_threshold(project)
    messages.success(request, 'Görev tamamlandı.')
    return redirect('projects:project_detail', pk=project.pk)
