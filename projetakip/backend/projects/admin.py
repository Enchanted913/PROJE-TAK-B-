from django.contrib import admin

from .models import Project, ProjectGrade, Task, TaskProgress


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'status', 'created_at')
    list_filter = ('status', 'teacher')
    filter_horizontal = ('students',)
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'order')
    list_filter = ('project',)


@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'status', 'started_at', 'completed_at')
    list_filter = ('status',)


@admin.register(ProjectGrade)
class ProjectGradeAdmin(admin.ModelAdmin):
    list_display = ('project', 'student', 'score')
