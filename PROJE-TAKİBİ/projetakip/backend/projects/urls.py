from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('', views.project_list, name='project_list'),
    path('add/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:pk>/complete/', views.project_complete, name='project_complete'),
    path('<int:project_pk>/tasks/add/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:project_pk>/grade/<int:student_pk>/', views.grade_student, name='grade_student'),
    path('progress/<int:pk>/start/', views.task_start, name='task_start'),
    path('progress/<int:pk>/complete/', views.task_complete, name='task_complete'),
]
